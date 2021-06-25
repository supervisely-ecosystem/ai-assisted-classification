import supervisely_lib as sly
import globals as g
import cache
import figure_utils
import prediction
import ui


@g.my_app.callback("connect")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def connect(api: sly.Api, task_id, context, state, app_logger):
    try:
        g.model_info = api.task.send_request(state["sessionId"], "get_session_info", data={})
        g.model_meta = sly.ProjectMeta.from_json(
            api.task.send_request(state["sessionId"], "get_model_meta", data={})
        )
        g.tags_examples = api.task.send_request(state["sessionId"], "get_tags_examples", data={})
        ui.set_model_info(task_id, api, g.model_info, g.model_meta.tag_metas, g.tags_examples)
    except Exception as e:
        api.task.set_field(task_id, "state.connecting", False)
        raise e


@g.my_app.callback("next_object")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def next_object(api: sly.Api, task_id, context, state, app_logger):
    sly.logger.debug("Context", extra={"context": context})
    project_id = context["projectId"]
    image_id = context["imageId"]
    figure_id = context["figureId"]
    ann_tool_session = context["sessionId"]

    ann = cache.get_annotation(project_id, image_id)

    if len(ann.labels) == 0:
        g.my_app.show_modal_window("There are no figures on image")
        return

    next_figure_id = figure_utils.get_next(ann, figure_id)
    if next_figure_id is not None:
        api.img_ann_tool.set_figure(ann_tool_session, next_figure_id)
        api.img_ann_tool.zoom_to_figure(ann_tool_session, next_figure_id, zoom_factor=2)
        results = figure_utils.classify(state["sessionId"], image_id, state["topn"], ann, next_figure_id)
        prediction.show(results)
    else:
        g.my_app.show_modal_window("All figures are visited. Select another figure or clear selection to iterate over objects again")
        prediction.hide()


@g.my_app.callback("clear_cache")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def clear_cache(api: sly.Api, task_id, context, state, app_logger):
    cache.clear()


@g.my_app.callback("manual_selected_image_changed")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def image_changed(api: sly.Api, task_id, context, state, app_logger):
    if state["applyTo"] == "object":
        return


@g.my_app.callback("manual_selected_figure_changed")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def figure_changed(api: sly.Api, task_id, context, state, app_logger):
    sly.logger.debug("Context", extra={"context": context})
    if state["applyTo"] == "image":
        return

    figure_id = context.get("figureId", None)
    if figure_id is None:
        sly.logger.debug("Selected figure is None")
        return

    project_id = context["projectId"]
    image_id = context["imageId"]
    figure_id = context["figureId"]
    nn_session = state["sessionId"]

    ann = cache.get_annotation(project_id, image_id)
    results = figure_utils.classify(nn_session, image_id, state["topn"], ann, figure_id)
    prediction.show(results)


@g.my_app.callback("disconnect")
@sly.timeit
def disconnect(api: sly.Api, task_id, context, state, app_logger):
    new_data = {}
    new_state = {}
    ui.init(new_data, new_state)
    cache.clear()
    fields = [
        {"field": "data", "payload": new_data, "append": True},
        {"field": "state", "payload": new_state, "append": True},
    ]
    api.task.set_fields(task_id, fields)


@g.my_app.callback("assign_to_object")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def assign_to_object(api: sly.Api, task_id, context, state, app_logger):
    try:
        project_id = context["projectId"]
        figure_id = context["figureId"]
        class_name = state["assignName"]
        figure_utils.assign_to_object(project_id, figure_id, class_name)
        api.task.set_field(g.task_id, "state.assignLoading", False)
    except Exception as e:
        api.task.set_field(g.task_id, "state.assignLoading", False)
        raise e


def main():
    data = {}
    state = {}

    ui.init(data, state)

    g.my_app.run(data=data, state=state)


#@TODO: unknown tag manually - show usage and explain in readme
#@TODO: image mode
#@TODO: Predictions will be shown here - add button refresh (select object or refresh???)
#@TODO: iterate object - creation order - add to readme
#@TODO: get errors from serve
#@TODO: connect loading ...
if __name__ == "__main__":
    sly.main_wrapper("main", main)
