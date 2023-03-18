from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.urls import path

from .enums import PackViews
from .views import CreateView, DeleteView, DetailView, ListView, UpdateView

ALL_FIELDS = "__all__"

ALL_VIEWS = {
    PackViews.LIST: ListView,
    PackViews.CREATE: CreateView,
    PackViews.UPDATE: UpdateView,
    PackViews.DETAIL: DetailView,
    PackViews.DELETE: DeleteView,
}


class ModelPack:
    # Views
    model = None
    # Used on Create and Update views
    form_class = None
    # User for passed to Create and Update views for generate forms
    fields = None
    # Used for create ListView with de specified fields
    list_fields = ("__str__",)
    # Used for create DetailView with specified fields
    detail_fields = ()
    allow_views = (
        "list",
        "create",
        "update",
        "detail",
        "delete",
    )
    create_success_url = "list"
    update_success_url = "list"
    delete_success_url = "list"

    # Context
    # list_extra_context = {}
    form_extra_context = {}
    detail_extra_context = {}

    # Inlines
    inlines = {}

    # Templates
    list_template_name = None  # Says which list template use
    form_template_name = None  # Says which form template use
    detail_template_name = None  # Says which detail template use
    delete_template_name = None  # Says which delete template use
    _template_names = None

    # Mixins
    list_mixins = ()  # List of mixins that include in ListViews
    form_mixins = ()  # List of mixins that include in Create and Update Views
    detail_mixins = ()  # List of mixins that include in DetailViews
    delete_mixins = ()  # List of mixins that include in DetailViews

    # Prepopulate
    # slug_field = "slug"
    # prepopulate_slug = ()

    # Options for build queryset
    queryset = None  # Specified custom queryset
    paginate_by = None  # Specified if ListView paginated by

    # Filter and ordering
    # search_fields = ()  # Used for create searchs method by specified fields
    # filter_fields = ()
    # order_by = ()  # User for crate ordering methods by specified fields

    # Urls
    url_list_suffix = "list"
    url_create_suffix = "create"
    url_update_suffix = "update"
    url_detail_suffix = "detail"
    url_delete_suffix = "delete"

    def __init__(self, model, **kwargs):
        if not model:
            error = "The 'model' attribute must be specified."
            raise ImproperlyConfigured(error)

        if not isinstance(self.detail_fields, (tuple, list, dict)):
            raise ImproperlyConfigured(
                "The 'detail_fields' must be an instance of tuple, list or dict"  # NOQA: E501
            )

        self.model = model

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._template_names = {
            PackViews.LIST: self.list_template_name,
            PackViews.CREATE: self.form_template_name,
            PackViews.UPDATE: self.form_template_name,
            PackViews.DETAIL: self.detail_template_name,
            PackViews.DELETE: self.delete_template_name,
        }

        if not isinstance(self.queryset, QuerySet):
            self.queryset = self.model._default_manager.all()

        if not isinstance(self.allow_views, tuple):
            error = "The 'allow_views' attribute must be a tuple."
            raise ImproperlyConfigured(error)

        if not self.form_class and not self.fields:
            self.fields = ALL_FIELDS

    @property
    def model_info(self):
        return self.model._meta.app_label, self.model._meta.model_name

    def get_base_url_name(self, suffix):
        url_suffix = getattr(self, "url_%s_suffix" % suffix)
        base_url_name = "%s_%s_%s" % (*self.model_info, url_suffix)
        return base_url_name

    def get_url_name(self, suffix):
        url_name = "pack:%s" % self.get_base_url_name(suffix)
        return url_name

    def get_urls(self):
        urlpatterns = []

        for enum in PackViews:
            url_name = self.get_base_url_name(enum.value)
            route = "{0}/{1}/".format(enum.param, enum.suffix)
            route = route.replace("//", "/")
            route = route.lstrip("/") if route.startswith("/") else route
            View = ALL_VIEWS.get(enum)
            urlpatterns += [
                path(route=route, view=View.as_view(pack=self), name=url_name)
            ]

        return urlpatterns

    def get_paths(self, instance=None):
        paths = {}

        for enum in PackViews:
            path = "/{0}/{1}/{2}/{3}/".format(
                *self.model_info,
                enum.kwarg,
                enum.suffix,
            )
            path = path.replace("//", "/").replace("//", "/")

            if instance:
                path = path.format(**instance.__dict__)

            paths.update({enum.name.lower(): path})

        return paths

    @property
    def urls(self):
        return self.get_urls()

    @property
    def paths(self):
        return self.get_paths()