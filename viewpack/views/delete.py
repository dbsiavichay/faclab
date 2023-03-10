from django.views.generic import DeleteView as BaseDeleteView
from django.views.generic import View

from .base import get_base_view


class DeleteMixin:
    def get_success_url(self):
        paths = self.pack.paths
        return paths.get(self.pack.delete_success_url)


class DeleteView(View):
    pack = None

    def view(self, request, *args, **kwargs):
        mixins = [DeleteMixin]
        View = get_base_view(BaseDeleteView, mixins, self.pack)

        View.__bases__ = (*self.pack.delete_mixins, *View.__bases__)
        view = View.as_view()
        return view(request, *args, **kwargs)
