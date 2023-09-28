def resetStates(d):
    for key, value in d.items():
        if isinstance(value, dict):
            resetStates(value)
        else:
            d[key] = None
