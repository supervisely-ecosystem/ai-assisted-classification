from pathlib import Path
import sys
import os
import supervisely_lib as sly

root_source_dir = str(Path(sys.argv[0]).parents[1])
sly.logger.info(f"Root source directory: {root_source_dir}")
sys.path.append(root_source_dir)
source_path = str(Path(sys.argv[0]).parents[0])
sly.logger.info(f"App source directory: {source_path}")
sys.path.append(source_path)
ui_sources_dir = os.path.join(source_path, "ui")
sly.logger.info(f"UI source directory: {ui_sources_dir}")
sys.path.append(ui_sources_dir)
sly.logger.info(f"Added to sys.path: {ui_sources_dir}")

owner_id = int(os.environ['context.userId'])
team_id = int(os.environ['context.teamId'])

my_app: sly.AppService = sly.AppService(ignore_task_id=True)
api = my_app.public_api
task_id = my_app.task_id

model_meta: sly.ProjectMeta = None
model_info = None
tags_examples = None
examples_data = None
model_tag_names = None

cache_path = os.path.join(my_app.data_dir, "cache")
sly.fs.mkdir(cache_path)

unknown_tag_meta = sly.TagMeta("unknown", sly.TagValueType.NONE, color=[255,165,0])