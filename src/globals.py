import pathlib
import sys
import os
import supervisely_lib as sly

root_source_path = str(pathlib.Path(sys.argv[0]).parents[2])
sly.logger.info(f"Root source directory: {root_source_path}")
sys.path.append(root_source_path)

owner_id = int(os.environ['context.userId'])
team_id = int(os.environ['context.teamId'])

my_app: sly.AppService = sly.AppService(ignore_task_id=True)
api = my_app.public_api
task_id = my_app.task_id

model_meta: sly.ProjectMeta = None
model_info = None
labels_urls = None
