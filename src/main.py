import supervisely_lib as sly
import globals as g
import cache
import figure_utils
import prediction
import ui
import info_tab
import review_tab


def handle_model_errors(data):
    if "error" in data:
        raise RuntimeError(data["error"])
    return data


@g.my_app.callback("connect")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def connect(api: sly.Api, task_id, context, state, app_logger):
    try:
        g.model_info = handle_model_errors(
            api.task.send_request(state["nnId"], "get_session_info", data={})
        )
        model_meta_json = handle_model_errors(
            api.task.send_request(state["nnId"], "get_model_meta", data={})
        )
        g.model_meta = sly.ProjectMeta.from_json(model_meta_json)
        g.tags_examples = handle_model_errors(
            api.task.send_request(state["nnId"], "get_tags_examples", data={})
        )
        info_tab.set_model_info(task_id, api, g.model_info, g.model_meta.tag_metas, g.tags_examples)
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
        results = figure_utils.classify(state["nnId"], image_id, state["topn"], ann, next_figure_id, state["pad"])
        prediction.show(results)
        review_tab.refresh_figure(project_id, next_figure_id)
    else:
        g.my_app.show_modal_window("All figures are visited. Select another figure or clear selection to iterate over objects again")
        prediction.hide()
        review_tab.reset()


@g.my_app.callback("manual_selected_image_changed")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def image_changed(api: sly.Api, task_id, context, state, app_logger):
    nn_session = state["nnId"]
    if nn_session is None:
        return
    if state["applyTo"] == "object":
        return


@g.my_app.callback("manual_selected_figure_changed")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def figure_changed(api: sly.Api, task_id, context, state, app_logger):
    project_id = context["projectId"]
    nn_session = state["nnId"]
    if nn_session is None:
        return

    sly.logger.debug("Context", extra={"context": context})
    if state["applyTo"] == "image":
        return

    figure_id = context.get("figureId", None)
    if figure_id is None:
        sly.logger.debug("Selected figure is None")
        prediction.hide()
        review_tab.reset()
        return

    project_id = context["projectId"]
    image_id = context["imageId"]
    figure_id = context["figureId"]

    ann = cache.get_annotation(project_id, image_id)
    results = figure_utils.classify(nn_session, image_id, state["topn"], ann, figure_id, state["pad"])
    prediction.show(results)
    review_tab.refresh_figure(project_id, figure_id)


@g.my_app.callback("disconnect")
@sly.timeit
def disconnect(api: sly.Api, task_id, context, state, app_logger):
    new_data = {}
    new_state = {}
    ui.init(new_data, new_state)
    cache.clear()
    fields = [
        {"field": "data", "payload": new_data},
        {"field": "state", "payload": new_state},
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
        review_tab.refresh_figure(project_id, figure_id)
        fields = [
            {"field": "state.assignLoading", "payload": False},
            {"field": "state.previousName", "payload": class_name},
        ]
        api.task.set_fields(task_id, fields)
    except Exception as e:
        api.task.set_field(g.task_id, "state.assignLoading", False)
        raise e


@g.my_app.callback("predict")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def predict(api: sly.Api, task_id, context, state, app_logger):
    try:
        project_id = context["projectId"]
        image_id = context["imageId"]
        figure_id = context["figureId"]
        apply_to = state["applyTo"]
        nn_session = state["nnId"]

        if apply_to == "object":
            ann = cache.get_annotation(project_id, image_id)
            results = figure_utils.classify(nn_session, image_id, state["topn"], ann, figure_id, state["pad"])
            prediction.show(results)
            review_tab.refresh_figure(project_id, figure_id)
        elif apply_to == "image":
            raise NotImplementedError()

        api.task.set_field(g.task_id, "state.predictLoading", False)
    except Exception as e:
        api.task.set_field(g.task_id, "state.predictLoading", False)
        prediction.hide()
        raise e


@g.my_app.callback("mark_unknown")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def mark_unknown(api: sly.Api, task_id, context, state, app_logger):
    try:
        project_id = context["projectId"]
        image_id = context["imageId"]
        figure_id = context["figureId"]
        apply_to = state["applyTo"]

        if apply_to == "object":
            figure_utils._assign_tag_to_object(project_id, figure_id, g.unknown_tag_meta)
            review_tab.refresh_figure(project_id, figure_id)
        else:
            raise NotImplementedError()

        fields = [
            {"field": "state.assignLoading", "payload": False},
            {"field": "state.previousName", "payload": g.unknown_tag_meta.name},
        ]
        api.task.set_fields(task_id, fields)
    except Exception as e:
        api.task.set_field(g.task_id, "state.assignLoading", False)
        raise e


@g.my_app.callback("mark_as_previous")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def mark_as_previous(api: sly.Api, task_id, context, state, app_logger):
    try:
        project_id = context["projectId"]
        image_id = context["imageId"]
        figure_id = context["figureId"]
        apply_to = state["applyTo"]

        if apply_to == "object":
            figure_utils.assign_to_object(project_id, figure_id, state["previousName"])
            review_tab.refresh_figure(project_id, figure_id)
        else:
            raise NotImplementedError()
        api.task.set_field(g.task_id, "state.assignLoading", False)
    except Exception as e:
        api.task.set_field(g.task_id, "state.assignLoading", False)
        raise e


def main():
    g.my_app.compile_template(g.root_source_dir)

    data = {}
    state = {}
    ui.init(data, state)

    g.my_app.run(data=data, state=state)

#@TODO: append vs replace
#@TODO: remove tag in review
#@TODO: image mode
#@TODO: get errors from serve
if __name__ == "__main__":
    sly.main_wrapper("main", main)
