def interpolate(start, end, alpha, mode):
    if mode == "Linear":
        return start + (end - start) * alpha
    return end
