from django.views.generic import UpdateView as BaseUpdateView
from django.views.generic import View

from viewpack.enums import PackViews
from viewpack.mixins import InlineMixin

from .base import get_base_view


class UpdateMixin:
    name = PackViews.UPDATE

    def get_success_url(self):
        paths = self.pack.paths
        return paths.get(self.pack.update_success_url)


class UpdateView(View):
    pack = None

    def view(self, request, *args, **kwargs):
        mixins = [UpdateMixin]

        if self.pack.inlines:
            mixins.append(InlineMixin)

        View = get_base_view(BaseUpdateView, mixins, self.pack)
        View.form_class = self.pack.form_class
        View.fields = self.pack.fields
        View.__bases__ = (*self.pack.form_mixins, *View.__bases__)
        view = View.as_view()

        return view(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return self.view(request, *args, **kwargs)
