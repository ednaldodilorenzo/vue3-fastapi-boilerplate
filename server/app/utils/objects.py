def create_object_from_instance(instance, Class):
    result = Class()
    for var, value in vars(instance).items():
        _ = hasattr(result, var) and (value is not None) and setattr(result, var, value)

    return result


def transfer_attributes(instance, base):
    for var, value in vars(base).items():
        _ = var[0] != "_" and hasattr(instance, var) and (value is not None) and setattr(instance, var, value)
