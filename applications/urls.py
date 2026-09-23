from django.urls import path

from .views import (
    apply_job,
    my_applications,
    recruiter_applications,
    update_application_status,
    candidate_profile,
)


urlpatterns = [

    # Candidate - Apply Job
    path(
        "apply/<int:job_id>/",
        apply_job,
        name="apply_job"
    ),

    # Candidate - My Applications
    path(
        "my-applications/",
        my_applications,
        name="my_applications"
    ),

    # Recruiter - Applications
    path(
        "recruiter/",
        recruiter_applications,
        name="recruiter_applications"
    ),

    # Recruiter - Update Application Status
    path(
        "recruiter/status/<int:application_id>/",
        update_application_status,
        name="update_application_status"
    ),

    # Recruiter - Candidate Profile
    path(
        "recruiter/candidate/<int:application_id>/",
        candidate_profile,
        name="candidate_profile"
    ),
]
