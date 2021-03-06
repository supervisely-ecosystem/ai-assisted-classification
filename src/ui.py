from collections import defaultdict
import supervisely_lib as sly

import globals as g
import info_tab
import predictions_tab
import review_tab
import settings_tab


def init(data, state):
    state["loading"] = False

    # state["connecting"] = False
    # state["nextLoading"] = False

    data["ownerId"] = g.owner_id
    data["teamId"] = g.team_id
    data["ssOptions"] = {
        "sessionTags": ["deployed_nn_cls"],
        "showLabel": False,
        "size": "small"
    }
    data["connected"] = False
    state["nnId"] = None  # task id of deployed model
    state["tabName"] = "info"

    info_tab.init(data, state)
    predictions_tab.init(data, state)
    review_tab.init(data, state)
    settings_tab.init(data, state)

    state["assignLoading"] = False
    state["assignName"] = None

    state["predictLoading"] = False


