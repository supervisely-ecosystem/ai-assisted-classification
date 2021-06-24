import globals as g


def init(data, state):
    data["ownerId"] = g.owner_id
    data["teamId"] = g.team_id
    data["ssOptions"] = {
        "sessionTags": ["deployed_nn_cls"],
        "showLabel": False,
        "size": "mini"
    }
    state["sessionId"] = 5857  # None @TODO: for debug

    data["info"] = None
    data["tags"] = None
    data["connected"] = False
    # data["connectionError"] = ""
    # data["rollbackIds"] = []
    # data["ssOptions"] = {
    #     "sessionTags": ["deployed_nn"],
    #     "showLabel": False,
    #     "size": "mini"
    # }

    state["sessionId"] = ""
    state["classes"] = []
    state["tags"] = []
    state["tabName"] = "info"
    state["suffix"] = "model"
    state["settings"] = "# empty"
    state["addMode"] = "merge"
    state["processing"] = False

    state["activeNames"] = []


