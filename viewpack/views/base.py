def get_base_view(ClassView, mixins, pack):
    class View(ClassView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            config = {
                "title": self.model._meta.verbose_name_plural,
                "app_name": self.model._meta.app_label,
                "model_name": self.model._meta.model_name,
            }

            if "pack" in context:
                context["pack"].update(config)
            else:
                context.update({"pack": config})

            return context

        def get_template_names(self):
            self.template_name = self.pack._template_names.get(self.name)

            return super().get_template_names()

    View.__bases__ = (*mixins, *View.__bases__)
    View.pack = pack
    View.model = pack.model
    View.queryset = pack.queryset

    return View
