import globals as g
import supervisely_lib as sly


def show(results):
    pred_tags_names = []
    pred_tags = []
    for item in results:
        tag_meta = g.model_meta.tag_metas.get(item["class"])
        if tag_meta is None:
            raise KeyError(f"Predicted tag with name \"{item['class']}\" not found in model meta")
        tag_meta_json = tag_meta.to_json()
        tag_meta_json["score"] = "{:.3f}".format(item["score"])
        pred_tags.append(tag_meta_json)
        pred_tags_names.append(tag_meta.name)

    fields = [
        {"field": "data.predTags", "payload": pred_tags},
        {"field": "data.predTagsNames", "payload": pred_tags_names},
        {"field": "state.activeNamesPred", "payload": pred_tags_names}
    ]
    g.api.task.set_fields(g.task_id, fields)


def hide():
    g.api.task.set_field(g.task_id, "data.predictions", None)