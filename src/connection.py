import supervisely_lib as sly
import globals as g
import info_tab
import ui
import cache


def handle_model_errors(data):
    if "error" in data:
        raise RuntimeError(data["error"])
    return data


@g.my_app.callback("connect")
@sly.timeit
@g.my_app.ignore_errors_and_show_dialog_window()
def connect(api: sly.Api, task_id, context, state, app_logger):
    try:
        fields = {
            "state.loading": False
        }
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
        info_tab.set_model_info(task_id, api, g.model_info, g.model_meta.tag_metas, g.tags_examples, fields)
        api.task.set_fields_from_dict(task_id, fields)
    except Exception as e:
        api.task.set_fields_from_dict(task_id, fields)
        raise e


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