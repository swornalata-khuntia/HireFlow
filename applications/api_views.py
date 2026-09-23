from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied
)

from .models import Application
from .api_serializers import ApplicationSerializer

from jobs.models import Job
from resume_analyzer.models import Resume


# ==========================================================
# NORMAL WEBSITE - APPLY FOR JOB
# ==========================================================

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    Application.objects.get_or_create(
        user=request.user,
        job=job
    )

    return redirect(
        "my_applications"
    )


# ==========================================================
# NORMAL WEBSITE - MY APPLICATIONS
# ==========================================================

@login_required
def my_applications(request):

    applications = Application.objects.filter(
        user=request.user
    ).select_related(
        "job"
    ).order_by(
        "-applied_at"
    )

    context = {
        "applications": applications
    }

    return render(
        request,
        "applications/my_applications.html",
        context
    )


# ==========================================================
# NORMAL WEBSITE - RECRUITER APPLICATIONS
# ==========================================================

@login_required
def recruiter_applications(request):

    try:
        profile = request.user.profile

    except Exception:
        return redirect(
            "dashboard"
        )

    if profile.role != "recruiter":
        return redirect(
            "dashboard"
        )

    company_name = profile.company_name

    applications = Application.objects.filter(
        job__company=company_name
    ).select_related(
        "user",
        "job"
    ).order_by(
        "-applied_at"
    )

    context = {
        "applications": applications,
        "company_name": company_name,
    }

    return render(
        request,
        "applications/recruiter_applications.html",
        context
    )


# ==========================================================
# NORMAL WEBSITE - UPDATE APPLICATION STATUS
# ==========================================================

@login_required
def update_application_status(
    request,
    application_id
):

    try:
        profile = request.user.profile

    except Exception:
        return redirect(
            "dashboard"
        )

    if profile.role != "recruiter":
        return redirect(
            "dashboard"
        )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=profile.company_name
    )

    if request.method == "POST":

        status = request.POST.get(
            "status"
        )

        valid_statuses = [
            "Applied",
            "Shortlisted",
            "Interview",
            "Selected",
            "Rejected",
        ]

        if status in valid_statuses:

            application.status = status

            application.save()

    return redirect(
        "recruiter_applications"
    )


# ==========================================================
# NORMAL WEBSITE - RECRUITER VIEW CANDIDATE PROFILE
# ==========================================================

@login_required
def candidate_profile(
    request,
    application_id
):

    try:
        profile = request.user.profile

    except Exception:
        return redirect(
            "dashboard"
        )

    if profile.role != "recruiter":
        return redirect(
            "dashboard"
        )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=profile.company_name
    )

    candidate = application.user

    resume = Resume.objects.filter(
        user=candidate
    ).order_by(
        "-uploaded_at"
    ).first()

    skills = [
        "Python",
        "Java",
        "Django",
        "HTML",
        "CSS",
        "JavaScript",
        "MySQL",
        "SQL",
        "React",
        "Git",
        "GitHub",
        "REST API",
        "C++",
        "C",
        "Spring Boot",
        "MongoDB",
        "Node.js",
        "Express.js",
        "Bootstrap",
        "Docker",
    ]

    detected_skills = []

    resume_score = 0

    if resume:

        resume_text = (
            resume.extracted_text or ""
        ).lower()

        for skill in skills:

            if skill.lower() in resume_text:

                detected_skills.append(
                    skill
                )

        if len(skills) > 0:

            resume_score = round(
                (
                    len(detected_skills)
                    / len(skills)
                ) * 100
            )

    context = {
        "application": application,
        "candidate": candidate,
        "candidate_profile": getattr(
            candidate,
            "profile",
            None
        ),
        "resume": resume,
        "detected_skills": detected_skills,
        "resume_score": resume_score,
    }

    return render(
        request,
        "applications/candidate_profile.html",
        context
    )


# ==========================================================
# REST API - MY APPLICATIONS
# ==========================================================

class MyApplicationsAPIView(
    generics.ListAPIView
):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Application.objects.filter(
            user=self.request.user
        ).select_related(
            "user",
            "job"
        ).order_by(
            "-applied_at"
        )


# ==========================================================
# REST API - APPLY FOR JOB
# ==========================================================

class ApplicationCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer
    ):

        job_id = self.kwargs.get(
            "job_id"
        )

        job = get_object_or_404(
            Job,
            id=job_id
        )

        already_applied = Application.objects.filter(
            user=self.request.user,
            job=job
        ).exists()

        if already_applied:

            raise ValidationError(
                {
                    "detail":
                    "You have already applied for this job."
                }
            )

        serializer.save(
            user=self.request.user,
            job=job
        )


# ==========================================================
# REST API - RECRUITER APPLICATIONS
# ==========================================================

class RecruiterApplicationsAPIView(
    generics.ListAPIView
):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        try:
            profile = self.request.user.profile

        except Exception:

            raise PermissionDenied(
                "User profile not found."
            )

        if profile.role != "recruiter":

            raise PermissionDenied(
                "Only recruiters can view applications."
            )

        return Application.objects.filter(
            job__company=profile.company_name
        ).select_related(
            "user",
            "job"
        ).order_by(
            "-applied_at"
        )


# ==========================================================
# REST API - UPDATE APPLICATION STATUS
# ==========================================================

class RecruiterApplicationStatusAPIView(
    generics.UpdateAPIView
):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    http_method_names = [
        "put",
        "patch"
    ]

    def get_queryset(self):

        try:
            profile = self.request.user.profile

        except Exception:

            raise PermissionDenied(
                "User profile not found."
            )

        if profile.role != "recruiter":

            raise PermissionDenied(
                "Only recruiters can update application status."
            )

        return Application.objects.filter(
            job__company=profile.company_name
        ).select_related(
            "user",
            "job"
        )