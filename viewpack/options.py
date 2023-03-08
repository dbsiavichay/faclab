from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.urls import path

from .views import CreateView, DeleteView, DetailView, ListView, UpdateView

ALL_FIELDS = "__all__"


class ModelPack:
    # Views
    model = None
    form_class = None  # Used on Create and Update views
    fields = None  # User for passed to Create and Update views for generate forms
    list_fields = ("__str__",)  # Used for create ListView with de specified fields
    detail_fields = ()  # Used for create DetailView with specified fields
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
    list_extra_context = {}
    form_extra_context = {}
    detail_extra_context = {}

    # Inlines
    inlines = {}

    # Templates
    list_template_name = None  # Says which list template use
    form_template_name = None  # Says which form template use
    detail_template_name = None  # Says which detail template use
    delete_template_name = None  # Says which delete template use

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
            raise ImproperlyConfigured("The 'model' attribute must be specified.")

        self.model = model

        for key, value in kwargs.items():
            setattr(self, key, value)

        if not isinstance(self.queryset, QuerySet):
            self.queryset = self.model._default_manager.all()

        if not isinstance(self.allow_views, tuple):
            raise ImproperlyConfigured("The 'allow_views' attribute must be a tuple.")

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

        # has_slug = hasattr(self.model, self.slug_field)
        has_slug = False
        route_param = "<slug:slug>" if has_slug else "<int:pk>"

        if "list" in self.allow_views:
            url_name = self.get_base_url_name("list")
            urlpatterns += [
                path(route="", view=ListView.as_view(site=self), name=url_name)
            ]

        if "create" in self.allow_views:
            url_create_name = self.get_base_url_name("create")

            urlpatterns += [
                path(
                    route=f"{self.url_create_suffix}/",
                    view=CreateView.as_view(site=self),
                    name=url_create_name,
                ),
            ]

        if "update" in self.allow_views:
            url_update_name = self.get_base_url_name("update")

            urlpatterns += [
                path(
                    route=f"{route_param}/{self.url_update_suffix}/",
                    view=UpdateView.as_view(site=self),
                    name=url_update_name,
                )
            ]

        if "detail" in self.allow_views:
            url_detail_name = self.get_base_url_name("detail")
            urlpatterns += [
                path(
                    route=f"{route_param}/{self.url_detail_suffix}/",
                    view=DetailView.as_view(site=self),
                    name=url_detail_name,
                ),
            ]

        if "delete" in self.allow_views:
            url_delete_name = self.get_base_url_name("delete")

            urlpatterns += [
                path(
                    route=f"{route_param}/{self.url_delete_suffix}/",
                    view=DeleteView.as_view(site=self),
                    name=url_delete_name,
                ),
            ]

        return urlpatterns

    def get_paths(self):
        paths = {}

        actions = (
            ("create", ""),
            ("list", ""),
            ("update", "pk"),
            ("detail", "pk"),
            ("delete", "pk"),
        )

        for action, kwarg in actions:
            path = "/%s/%s/{kwarg}/%s" % (*self.model_info, kwarg, action)
            path = path.replace("//", "/")
            paths.update({action: path})

        return paths

    @property
    def urls(self):
        return self.get_urls()

    @property
    def paths(self):
        return self.get_paths()
