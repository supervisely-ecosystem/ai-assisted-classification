def init(data, state):
    state["activeNames"] = []
    state["activeNamesPred"] = []
    data["predTags"] = None
    data["predTagsNames"] = None

    state["previousName"] = None