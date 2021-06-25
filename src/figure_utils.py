import supervisely_lib as sly
import globals as g
import cache


def get_next(ann: sly.Annotation, cur_figure_id):
    if len(ann.labels) == 0:
        return None
    if cur_figure_id is None:
        # nothing is selected, return first figure
        return ann.labels[0].geometry.sly_id
    else:
        for idx, label in enumerate(ann.labels):
            if cur_figure_id == label.geometry.sly_id:
                if idx == len(ann.labels) - 1:
                    # all labels are visited
                    return None
                else:
                    return ann.labels[idx + 1].geometry.sly_id


def classify(anntool_session_id, image_id, topn, ann: sly.Annotation, figure_id, pad):
    if figure_id is None:
        raise RuntimeError("figure_id is None")
    label = ann.get_label_by_id(figure_id)
    if label is None:
        raise ValueError(f"Label with id={figure_id} not found. Maybe cached annotation differs from the actual one. "
                         f"Please clear cache on settings tab")
    rect: sly.Rectangle = label.geometry.to_bbox()
    bounds = [rect.top, rect.left, rect.bottom, rect.right]

    predictions = g.api.task.send_request(anntool_session_id, "inference_image_id",
                                         data={
                                             "rectangle": bounds,
                                             "image_id": image_id,
                                             "topn": topn,
                                             "pad": pad
                                         })
    return predictions


def assign_to_object(project_id, figure_id, class_name):
    project_meta = cache.get_meta(project_id)
    tag_meta: sly.TagMeta = project_meta.get_tag_meta(class_name)
    if tag_meta is None:
        tag_meta = g.model_meta.tag_metas.get(class_name).clone()
        project_meta = project_meta.add_tag_meta(tag_meta)
        cache.update_project_meta(project_id, project_meta)
        project_meta = cache.get_meta(project_id)
        tag_meta = project_meta.get_tag_meta(class_name)
    g.api.advanced.add_tag_to_object(tag_meta.sly_id, figure_id)