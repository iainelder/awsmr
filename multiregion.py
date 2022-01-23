def multiregion(fn, *, region_names):

    if region_names is None or next(iter(region_names), None) is None:
        raise ValueError("region_names must be an iterable of at least one region name")

    def mr(*args, **kwargs):
        return [
            {
                "RegionName": rn,
                **response_or_exception(lambda: fn(*args, **kwargs, region_name=rn)),
            }
            for rn in region_names
        ]

    return mr


def response_or_exception(fn):
    try:
        return {"Response": fn()}
    except Exception as ex:
        return {"Exception": repr(ex)}
