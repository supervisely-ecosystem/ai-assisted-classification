import supervisely_lib as sly
import globals as g
import cache


def init(data, state):
    state["activeNamesReview"] = []
    data["reviewTags"] = None
    data["reviewTagsNames"] = None


def set_data(tags, tags_names, active_names):
    fields = [
        {"field": "state.activeNamesReview", "payload": list(set(active_names))},
        {"field": "data.reviewTags", "payload": tags},
        {"field": "data.reviewTagsNames", "payload": list(set(tags_names)) if tags_names is not None else tags_names},
    ]
    g.api.task.set_fields(g.task_id, fields)


def reset():
    set_data(tags=None, tags_names=None, active_names=[])


def refresh_figure(project_id, figure_id):
    if figure_id is None:
        reset()
    else:
        object_tags_json = g.api.advanced.get_object_tags(figure_id)
        project_meta = cache.get_meta(project_id)
        object_tags = sly.TagCollection.from_json(object_tags_json, project_meta.tag_metas)

        review_tags = []
        reviewTagsNames = []
        activeNamesReview = []
        for tag in object_tags:
            tag: sly.Tag
            tag_meta = project_meta.tag_metas.get(tag.meta.name)
            if tag_meta is not None:
                review_tags.append({**tag_meta.to_json(), "labelerLogin": tag.labeler_login})
                reviewTagsNames.append(tag_meta.name)
        set_data(review_tags, reviewTagsNames, activeNamesReview)
