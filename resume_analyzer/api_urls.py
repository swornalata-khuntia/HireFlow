from django.urls import path

from .api_views import MyResumeAPIView


urlpatterns = [

    path(
        "",
        MyResumeAPIView.as_view(),
        name="api_my_resumes"
    ),

]