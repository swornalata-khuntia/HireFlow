from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Job
from .forms import JobForm

from resume_analyzer.models import Resume


SKILLS = [
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


def detect_skills(text):
    text_lower = text.lower()
    detected = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            detected.append(skill)

    return detected


def calculate_match(resume_skills, required_skills):

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in [
            s.lower() for s in resume_skills
        ]:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(required_skills) > 0:

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

    else:
        match_percentage = 0

    return (
        match_percentage,
        matched_skills,
        missing_skills
    )


# =========================
# AI JOB MATCHES
# =========================

@login_required
def job_matches(request):

    latest_resume = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at").first()

    jobs = Job.objects.all()

    results = []
    resume_skills = []

    if latest_resume:

        resume_skills = detect_skills(
            latest_resume.extracted_text
        )

        for job in jobs:

            required_skills = [
                skill.strip()
                for skill in job.required_skills.split(",")
                if skill.strip()
            ]

            (
                match_percentage,
                matched_skills,
                missing_skills
            ) = calculate_match(
                resume_skills,
                required_skills
            )

            results.append({
                "job": job,
                "match_percentage": match_percentage,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            })

        results.sort(
            key=lambda x: x["match_percentage"],
            reverse=True
        )

    context = {
        "results": results,
        "latest_resume": latest_resume,
        "resume_skills": resume_skills,
    }

    return render(
        request,
        "jobs/job_matches.html",
        context
    )


# =========================
# RECRUITER - POST JOB
# =========================

@login_required
def post_job(request):

    try:
        profile = request.user.profile
    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.company = profile.company_name

            job.save()

            return redirect("recruiter_dashboard")

    else:

        form = JobForm()

    context = {
        "form": form,
        "company_name": profile.company_name,
    }

    return render(
        request,
        "jobs/post_job.html",
        context
    )


# =========================
# RECRUITER - MANAGE JOBS
# =========================

@login_required
def manage_jobs(request):

    try:
        profile = request.user.profile
    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

    jobs = Job.objects.filter(
        company=profile.company_name
    ).order_by("-created_at")

    context = {
        "jobs": jobs,
        "company_name": profile.company_name,
    }

    return render(
        request,
        "jobs/manage_jobs.html",
        context
    )


# =========================
# RECRUITER - EDIT JOB
# =========================

@login_required
def edit_job(request, job_id):

    try:
        profile = request.user.profile
    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        id=job_id,
        company=profile.company_name
    )

    if request.method == "POST":

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            updated_job = form.save(
                commit=False
            )

            updated_job.company = (
                profile.company_name
            )

            updated_job.save()

            return redirect("manage_jobs")

    else:

        form = JobForm(
            instance=job
        )

    context = {
        "form": form,
        "job": job,
        "company_name": profile.company_name,
    }

    return render(
        request,
        "jobs/edit_job.html",
        context
    )


# =========================
# RECRUITER - DELETE JOB
# =========================

@login_required
def delete_job(request, job_id):

    try:
        profile = request.user.profile
    except Exception:
        return redirect("dashboard")

    if profile.role != "recruiter":
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        id=job_id,
        company=profile.company_name
    )

    if request.method == "POST":

        job.delete()

    return redirect("manage_jobs")