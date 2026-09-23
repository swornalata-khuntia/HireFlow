from django.urls import path

from .api_views import (
    MyApplicationsAPIView,
    ApplicationCreateAPIView,
    RecruiterApplicationsAPIView,
    RecruiterApplicationStatusAPIView,
)


urlpatterns = [

    # ==================================================
    # CANDIDATE - MY APPLICATIONS
    # ==================================================

    path(
        "",
        MyApplicationsAPIView.as_view(),
        name="api_my_applications"
    ),

    # ==================================================
    # CANDIDATE - APPLY FOR JOB
    # ==================================================

    path(
        "apply/<int:job_id>/",
        ApplicationCreateAPIView.as_view(),
        name="api_apply_job"
    ),

    # ==================================================
    # RECRUITER - VIEW APPLICATIONS
    # ==================================================

    path(
        "recruiter/",
        RecruiterApplicationsAPIView.as_view(),
        name="api_recruiter_applications"
    ),

    # ==================================================
    # RECRUITER - UPDATE STATUS
    # ==================================================

    path(
        "recruiter/status/<int:pk>/",
        RecruiterApplicationStatusAPIView.as_view(),
        name="api_recruiter_application_status"
    ),

]