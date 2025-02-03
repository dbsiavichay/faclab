from django.urls import path

from .views import CertificateCreateView, CertificateDeleteView, CertificateListView

urlpatterns = [
    path("certificate/", CertificateListView.as_view(), name="certificate_list"),
    path(
        "certificate/create/",
        CertificateCreateView.as_view(),
        name="certificate_create",
    ),
    path(
        "certificate/<str:pk>/delete/",
        CertificateDeleteView.as_view(),
        name="certificate_delete",
    ),
]
