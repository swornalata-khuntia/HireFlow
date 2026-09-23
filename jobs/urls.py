from django.urls import path

from .views import (
    job_matches,
    post_job,
    manage_jobs,
    edit_job,
    delete_job,
)


urlpatterns = [

    # AI Job Matches
    path(
        "",
        job_matches,
        name="job_matches"
    ),

    # Recruiter - Post Job
    path(
        "post/",
        post_job,
        name="post_job"
    ),

    # Recruiter - Manage Jobs
    path(
        "manage/",
        manage_jobs,
        name="manage_jobs"
    ),

    # Recruiter - Edit Job
    path(
        "edit/<int:job_id>/",
        edit_job,
        name="edit_job"
    ),

    # Recruiter - Delete Job
    path(
        "delete/<int:job_id>/",
        delete_job,
        name="delete_job"
    ),
]