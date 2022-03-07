def is_same_params(params1, params2):
    params1 = dict(params1)
    params2 = dict(params2)
    try:
        del params1["clip_range"]
        del params2["clip_range"]
    except Exception:
        print("No Clip Range")
    return params1 == params2

