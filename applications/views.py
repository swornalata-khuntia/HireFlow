from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Application
from jobs.models import Job
from resume_analyzer.models import Resume


# =========================
# CANDIDATE - APPLY JOB
# =========================

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

    return redirect("my_applications")


# =========================
# CANDIDATE - MY APPLICATIONS
# =========================

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


# =========================
# RECRUITER - APPLICATIONS
# =========================

@login_required
def recruiter_applications(request):

    try:
        profile = request.user.profile

    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

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


# =========================
# RECRUITER - UPDATE STATUS
# =========================

@login_required
def update_application_status(
    request,
    application_id
):

    try:
        profile = request.user.profile

    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

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


# =========================
# RECRUITER - VIEW CANDIDATE
# =========================

@login_required
def candidate_profile(
    request,
    application_id
):

    try:
        profile = request.user.profile

    except Exception:
        return redirect("dashboard")

    # Only recruiter can access this page
    if profile.role != "recruiter":
        return redirect("dashboard")

    # Recruiter can only view candidates
    # who applied to their company's jobs
    application = get_object_or_404(
        Application,
        id=application_id,
        job__company=profile.company_name
    )

    candidate = application.user

    # Latest uploaded resume
    resume = Resume.objects.filter(
        user=candidate
    ).order_by(
        "-uploaded_at"
    ).first()

    # Resume skill detection
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

        # Simple resume score
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