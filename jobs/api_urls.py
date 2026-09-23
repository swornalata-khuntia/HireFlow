from django.urls import path

from .api_views import (
    JobListAPIView,
    JobDetailAPIView,
    JobCreateAPIView,
)


urlpatterns = [

    path(
        "create/",
        JobCreateAPIView.as_view(),
        name="api_job_create"
    ),

    path(
        "",
        JobListAPIView.as_view(),
        name="api_job_list"
    ),

    path(
        "<int:pk>/",
        JobDetailAPIView.as_view(),
        name="api_job_detail"
    ),

]