from django.apps import apps
from django.core.exceptions import ImproperlyConfigured


def register(model):
    """
    Register the given model(s) classes and wrapped ModelPack class:
    @register(Author)
    class AuthorPack(viewpack.ModelPack):
        pass
    """
    from viewpack import ModelPack, packs

    def _model_pack_wrapper(pack_cls):
        if not model:
            raise ValueError("One model must be passed to register.")

        model_class = None
        if isinstance(model, str):
            try:
                app_name, model_name = model.split(".")
                model_class = apps.get_model(app_name, model_name)
            except ValueError:
                raise ImproperlyConfigured("Does not exist '%s' model" % model)

        if not issubclass(pack_cls, ModelPack):
            raise ValueError("Wrapped class must subclass ModelPack.")

        packs.register(model_class if model_class else model, pack_cls=pack_cls)

        return pack_cls

    return _model_pack_wrapper
