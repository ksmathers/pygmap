def clamp(v, vmin, vmax):
    if v < vmin: v = vmin
    if v > vmax: v = vmax
    return v
