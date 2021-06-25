import supervisely_lib as sly


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
