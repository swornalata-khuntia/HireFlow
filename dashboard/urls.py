from django.urls import path
from .views import dashboard_view, recruiter_dashboard


urlpatterns = [
    path(
        "",
        dashboard_view,
        name="dashboard"
    ),

    path(
        "recruiter/",
        recruiter_dashboard,
        name="recruiter_dashboard"
    ),
]