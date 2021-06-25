import os
import pathlib
import sys
from collections import defaultdict
import supervisely_lib as sly
import globals as g
import cache
import figure_utils



import ui
# from shared_utils.connect import get_model_info
# from shared_utils.inference import postprocess


@g.my_app.callback("connect")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def connect(api: sly.Api, task_id, context, state, app_logger):
    global model_meta, model_info, tag_examples

    try:
        model_info = api.task.send_request(state["sessionId"], "get_session_info", data={})
        model_meta = sly.ProjectMeta.from_json(
            api.task.send_request(state["sessionId"], "get_model_meta", data={})
        )
        tags_examples = api.task.send_request(state["sessionId"], "get_tags_examples", data={})
        ui.set_model_info(task_id, api, model_info, model_meta.tag_metas, tags_examples)
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
    else:
        g.my_app.show_modal_window("All figures are visited. Select another figure or clear selection to iterate over objects again")



@g.my_app.callback("manual_selected_image_changed")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def image_changed(api: sly.Api, task_id, context, state, app_logger):
    pass


# @g.my_app.callback("disconnect")
# @sly.timeit
# def disconnect(api: sly.Api, task_id, context, state, app_logger):
#     global model_meta
#     model_meta = None
#
#     new_data = {}
#     new_state = {}
#     ui.init(new_data, new_state)
#     fields = [
#         {"field": "data", "payload": new_data, "append": True},
#         {"field": "state", "payload": new_state, "append": True},
#     ]
#     api.task.set_fields(task_id, fields)
#
#
# @g.my_app.callback("select_all_classes")
# @sly.timeit
# def select_all_classes(api: sly.Api, task_id, context, state, app_logger):
#     api.task.set_field(task_id, "state.classes", [True] * len(model_meta.obj_classes))
#
#
# @g.my_app.callback("deselect_all_classes")
# @sly.timeit
# def deselect_all_classes(api: sly.Api, task_id, context, state, app_logger):
#     api.task.set_field(task_id, "state.classes", [False] * len(model_meta.obj_classes))
#
#
# @g.my_app.callback("select_all_tags")
# @sly.timeit
# def select_all_tags(api: sly.Api, task_id, context, state, app_logger):
#     api.task.set_field(task_id, "state.tags", [True] * len(model_meta.tag_metas))
#
#
# @g.my_app.callback("deselect_all_tags")
# @sly.timeit
# def deselect_all_tags(api: sly.Api, task_id, context, state, app_logger):
#     api.task.set_field(task_id, "state.tags", [False] * len(model_meta.tag_metas))
#
#
# @g.my_app.callback("inference")
# @sly.timeit
# def inference(api: sly.Api, task_id, context, state, app_logger):
#     project_id = context["projectId"]
#     image_id = context["imageId"]
#
#     try:
#         inference_setting = yaml.safe_load(state["settings"])
#     except Exception as e:
#         inference_setting = {}
#         app_logger.warn(repr(e))
#
#     project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
#
#     if image_id not in ann_cache:
#         # keep only current image for simplicity
#         ann_cache.clear()
#
#     ann_json = api.annotation.download(image_id).annotation
#     ann = sly.Annotation.from_json(ann_json, project_meta)
#     ann_cache[image_id].append(ann)
#
#     ann_pred_json = api.task.send_request(state["sessionId"],
#                                           "inference_image_id",
#                                           data={
#                                               "image_id": image_id,
#                                               "settings": inference_setting
#                                           })
#     ann_pred = sly.Annotation.from_json(ann_pred_json, model_meta)
#     res_ann, res_project_meta = None, None #postprocess(api, project_id, ann_pred, project_meta, model_meta, state)
#
#     if state["addMode"] == "merge":
#         res_ann = ann.merge(res_ann)
#     else:
#         pass  # replace (data prepared, nothing to do)
#
#     if res_project_meta != project_meta:
#         api.project.update_meta(project_id, res_project_meta.to_json())
#     api.annotation.upload_ann(image_id, res_ann)
#     fields = [
#         {"field": "data.rollbackIds", "payload": list(ann_cache.keys())},
#         {"field": "state.processing", "payload": False}
#     ]
#     api.task.set_fields(task_id, fields)
#
#
# @g.my_app.callback("undo")
# @sly.timeit
# def undo(api: sly.Api, task_id, context, state, app_logger):
#     image_id = context["imageId"]
#     if image_id in ann_cache:
#         ann = ann_cache[image_id].pop()
#         if len(ann_cache[image_id]) == 0:
#             del ann_cache[image_id]
#         api.annotation.upload_ann(image_id, ann)
#
#     fields = [
#         {"field": "data.rollbackIds", "payload": list(ann_cache.keys())},
#         {"field": "state.processing", "payload": False}
#     ]
#     api.task.set_fields(task_id, fields)


def main():
    data = {}
    state = {}

    ui.init(data, state)

    g.my_app.run(data=data, state=state)


#@TODO: iterate object - creation order - add to readme
#@TODO: continue cache.get_image_path
#@TODO: get errors from serve
#@TODO: connect loading ...
if __name__ == "__main__":
    sly.main_wrapper("main", main)
