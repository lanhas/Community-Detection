
models = {}


def register(name):
    def decorate(cls):
        models[name] = cls
        return cls
    return decorate


def make(name, **kwargs):
    model = models[name](**kwargs)
    return model

