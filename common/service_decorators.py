

def only_field_decorator(service_func: callable):
    def only_field_warper(objects, only=(), **kwargs):
        return service_func(objects, **kwargs).only(*only)
    return only_field_warper
