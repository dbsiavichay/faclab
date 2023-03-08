from django.views.generic import UpdateView as BaseUpdateView
from django.views.generic import View

from .base import get_base_view


class UpdateMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.site.form_extra_context)

        return context

    def get_success_url(self):
        paths = self.pack.paths
        return paths.get(self.pack.update_success_url)


class UpdateView(View):
    def view(self, request, *args, **kwargs):
        mixins = [UpdateMixin]
        View = get_base_view(BaseUpdateView, mixins, self.pack)
        View.form_class = self.pack.form_class
        View.fields = self.pack.fields
        View.__bases__ = (*self.pack.form_mixins, *View.__bases__)
        view = View.as_view()

        return view(request, *args, **kwargs)
