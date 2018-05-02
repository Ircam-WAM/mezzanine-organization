def split_events_from_other_related_content(context, related_content):
    context["related"] = {}
    context["related"]["other"] = []
    context["related"]["event"] = []
    for rc in related_content:
        if rc.__class__.__name__ == "Event":
            context["related"]["event"].append(rc)
        else :
            context["related"]["other"].append(rc)
    return context        