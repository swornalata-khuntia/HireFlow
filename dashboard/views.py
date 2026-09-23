from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from jobs.models import Job
from resume_analyzer.models import Resume
from applications.models import Application


SKILLS = [
    "Python",
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


def calculate_match(
    resume_skills,
    required_skills
):

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in [
            resume_skill.lower()
            for resume_skill in resume_skills
        ]:

            matched_skills.append(skill)

    if len(required_skills) > 0:

        match_percentage = round(
            (
                len(matched_skills)
                / len(required_skills)
            ) * 100
        )

    else:

        match_percentage = 0

    return match_percentage


# ==================================================
# CANDIDATE DASHBOARD
# ==================================================

@login_required
def dashboard_view(request):

    latest_resume = Resume.objects.filter(
        user=request.user
    ).order_by(
        "-uploaded_at"
    ).first()


    all_applications = Application.objects.filter(
        user=request.user
    ).select_related(
        "job"
    ).order_by(
        "-applied_at"
    )


    applications_count = all_applications.count()


    interviews_count = all_applications.filter(
        status="Interview"
    ).count()


    recent_applications = all_applications[:4]


    recommended_jobs = []

    resume_skills = []


    if latest_resume:

        resume_skills = detect_skills(
            latest_resume.extracted_text
        )


        jobs = Job.objects.all()


        for job in jobs:

            required_skills = [
                skill.strip()
                for skill in job.required_skills.split(",")
                if skill.strip()
            ]


            match_percentage = calculate_match(
                resume_skills,
                required_skills
            )


            recommended_jobs.append({

                "job": job,

                "match_percentage":
                    match_percentage,

            })


        recommended_jobs.sort(
            key=lambda x:
                x["match_percentage"],
            reverse=True
        )


        recommended_jobs = (
            recommended_jobs[:3]
        )


    context = {

        "recommended_jobs":
            recommended_jobs,

        "latest_resume":
            latest_resume,

        "resume_skills":
            resume_skills,

        "applications_count":
            applications_count,

        "interviews_count":
            interviews_count,

        "recent_applications":
            recent_applications,

    }


    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ==================================================
# RECRUITER DASHBOARD
# ==================================================

@login_required
def recruiter_dashboard(request):

    try:

        profile = request.user.profile

    except Exception:

        return redirect("dashboard")


    if profile.role != "recruiter":

        return redirect("dashboard")


    company_name = profile.company_name


    # ----------------------------------------------
    # COMPANY JOBS
    # ----------------------------------------------

    company_jobs = Job.objects.filter(
        company=company_name
    ).order_by(
        "-created_at"
    )


    # ----------------------------------------------
    # COMPANY APPLICATIONS
    # ----------------------------------------------

    company_applications = (
        Application.objects
        .filter(
            job__company=company_name
        )
        .select_related(
            "user",
            "job"
        )
        .order_by(
            "-applied_at"
        )
    )


    # ----------------------------------------------
    # BASIC COUNTS
    # ----------------------------------------------

    total_jobs = company_jobs.count()

    total_applications = (
        company_applications.count()
    )


    shortlisted_count = (
        company_applications
        .filter(status="Shortlisted")
        .count()
    )


    interview_count = (
        company_applications
        .filter(status="Interview")
        .count()
    )


    selected_count = (
        company_applications
        .filter(status="Selected")
        .count()
    )


    rejected_count = (
        company_applications
        .filter(status="Rejected")
        .count()
    )


    applied_count = (
        company_applications
        .filter(status="Applied")
        .count()
    )


    # ----------------------------------------------
    # RECENT APPLICATIONS
    # ----------------------------------------------

    recent_applications = (
        company_applications[:6]
    )


    # ----------------------------------------------
    # JOB-WISE APPLICATION ANALYTICS
    # ----------------------------------------------

    job_application_stats = []


    for job in company_jobs:

        application_count = (
            Application.objects
            .filter(job=job)
            .count()
        )


        shortlisted = (
            Application.objects
            .filter(
                job=job,
                status="Shortlisted"
            )
            .count()
        )


        interviews = (
            Application.objects
            .filter(
                job=job,
                status="Interview"
            )
            .count()
        )


        selected = (
            Application.objects
            .filter(
                job=job,
                status="Selected"
            )
            .count()
        )


        job_application_stats.append({

            "job": job,

            "application_count":
                application_count,

            "shortlisted":
                shortlisted,

            "interviews":
                interviews,

            "selected":
                selected,

        })


    # ----------------------------------------------
    # ANALYTICS CONTEXT
    # ----------------------------------------------

    analytics = {

        "total_jobs":
            total_jobs,

        "total_applications":
            total_applications,

        "applied":
            applied_count,

        "shortlisted":
            shortlisted_count,

        "interviews":
            interview_count,

        "selected":
            selected_count,

        "rejected":
            rejected_count,

    }


    context = {

        # Existing recruiter data

        "profile":
            profile,

        "company_name":
            company_name,

        "company_jobs":
            company_jobs,

        "total_jobs":
            total_jobs,

        "total_applications":
            total_applications,

        "shortlisted_count":
            shortlisted_count,

        "interview_count":
            interview_count,

        "recent_applications":
            recent_applications,


        # New analytics data

        "selected_count":
            selected_count,

        "rejected_count":
            rejected_count,

        "applied_count":
            applied_count,

        "analytics":
            analytics,

        "job_application_stats":
            job_application_stats,

    }


    return render(
        request,
        "dashboard/recruiter_dashboard.html",
        context
    )