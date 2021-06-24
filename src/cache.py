import os
import supervisely_lib as sly
import globals as g

project2meta = {}  # project_id -> project_meta
image2info = {}
image2path = {}  # image_id -> image_path
image2ann = {}  # image_id -> annotation


def get_image_path(image_id):
    #@TODO: reimplement


    info = None
    if image_id not in image2info:
        info = g.api.image.get_info_by_id(image_id)
        image2info[image_id] = info
    else:
        info = image2info[image_id]

    local_path = os.path.join(g.cache_path, f"{info.id}{sly.fs.get_file_name_with_ext(info.name)}")
    if sly.fs.file_exists(local_path):
        return local_path
    else:
        g.api.image.download_path(image_id, local_path)
        image2path[image_id] = local_path
        return local_path

    info = g.api.image.get_info_by_id()


def get_annotation(image_id, ):
    pass