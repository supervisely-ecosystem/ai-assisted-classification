import supervisely_lib as sly
import globals as g


def init(data, state):
    data["info"] = None
    data["tags"] = None
    data["tagsExamples"] = None
    data["modelTagNames"] = None


def set_model_info(task_id, api, info, tag_metas, tags_examples):
    g.model_tag_names = []
    for tag_meta in tag_metas:
        tag_meta: sly.TagMeta
        if tag_meta.name not in tags_examples:
            sly.logger.warning(f"There are no examples for tag \"{tag_meta.name}\"")
            tags_examples[tag_meta.name] = []
        g.model_tag_names.append(tag_meta.name)

    g.examples_data = {}
    for name, urls in tags_examples.items():
        g.examples_data[name] = [{"moreExamples": [url], "preview": url} for url in urls]

    fields = [
        {"field": "data.connected", "payload": True},
        {"field": "state.connecting", "payload": False},
        {"field": "data.info", "payload": info},
        {"field": "data.tags", "payload": tag_metas.to_json()},
        {"field": "data.tagsExamples", "payload": g.examples_data},
        {"field": "data.modelTagNames", "payload": g.model_tag_names}
    ]
    api.app.set_fields(task_id, fields)
