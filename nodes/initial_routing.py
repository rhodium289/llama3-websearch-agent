# Conditional Routing Function
def conditional_routing(state):
    status = state["status"]
    if status == "valid":
        return "extract_enriched_data"
    elif status == "invalid":
        return "transform_query"
    else:
        raise ValueError("Invalid status")