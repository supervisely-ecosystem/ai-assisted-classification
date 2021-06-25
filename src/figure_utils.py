import supervisely_lib as sly
import globals as g


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


def classify(anntool_session_id, image_id, topn, ann: sly.Annotation, figure_id):
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
                                             "topn": topn
                                         })
    return predictions
    #@TODO: add predictions to object
    print(predictions)
    #[{'pred_label': 7, 'pred_score': 0.036875125020742416, 'pred_class': '173074'}, {'pred_label': 81, 'pred_score': 0.03571882098913193, 'pred_class': '173064'}, {'pred_label': 72, 'pred_score': 0.028079558163881302, 'pred_class': '198938'}, {'pred_label': 74, 'pred_score': 0.02756684087216854, 'pred_class': '127409'}, {'pred_label': 29, 'pred_score': 0.026954438537359238, 'pred_class': '198660'}]
    pass