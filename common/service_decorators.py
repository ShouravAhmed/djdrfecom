

def only_field_decorator(service_func: callable):
    def only_field_warper(model_name, objects, only=(), **kwargs):
        return service_func(model_name, objects, **kwargs).only(*only)
    return only_field_warper
