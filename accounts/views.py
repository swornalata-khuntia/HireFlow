from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from resume_analyzer.models import Resume
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# ==================================================
# SIGNUP
# ==================================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        role = request.POST.get(
            "role",
            "job_seeker"
        )

        company_name = request.POST.get(
            "company_name",
            ""
        ).strip()


        # ------------------------------------------
        # VALIDATION
        # ------------------------------------------

        if not username:

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Username is required."
                }
            )


        if not email:

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Email is required."
                }
            )


        if not password:

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Password is required."
                }
            )


        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Username already exists."
                }
            )


        # ------------------------------------------
        # ROLE VALIDATION
        # ------------------------------------------

        if role not in [
            "job_seeker",
            "recruiter"
        ]:

            role = "job_seeker"


        # ------------------------------------------
        # RECRUITER COMPANY VALIDATION
        # ------------------------------------------

        if role == "recruiter" and not company_name:

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Company name is required for recruiters."
                }
            )


        # ------------------------------------------
        # CREATE USER
        # ------------------------------------------

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )


        # ------------------------------------------
        # CREATE PROFILE
        # ------------------------------------------

        UserProfile.objects.create(

            user=user,

            role=role,

            company_name=company_name
            if role == "recruiter"
            else ""

        )


        # ------------------------------------------
        # LOGIN
        # ------------------------------------------

        login(
            request,
            user
        )


        # ------------------------------------------
        # REDIRECT
        # ------------------------------------------

        if role == "recruiter":

            return redirect(
                "recruiter_dashboard"
            )


        return redirect(
            "dashboard"
        )


    return render(
        request,
        "accounts/signup.html"
    )


# ==================================================
# LOGIN
# ==================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            try:

                profile = user.profile

                if profile.role == "recruiter":

                    return redirect(
                        "recruiter_dashboard"
                    )

            except Exception:

                pass


            return redirect(
                "dashboard"
            )


        return render(
            request,
            "accounts/login.html",
            {
                "error":
                "Invalid username or password."
            }
        )


    return render(
        request,
        "accounts/login.html"
    )


# ==================================================
# LOGOUT
# ==================================================

def logout_view(request):

    logout(request)

    return redirect("home")


# ==================================================
# CANDIDATE PROFILE
# ==================================================

@login_required
def candidate_profile_view(request):

    user = request.user


    try:

        profile = user.profile

    except UserProfile.DoesNotExist:

        profile = UserProfile.objects.create(

            user=user,

            role="job_seeker"

        )


    # ------------------------------------------
    # UPDATE PROFILE
    # ------------------------------------------

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()


        user.email = email

        user.save()


        profile.phone = phone

        profile.save()


        return redirect(
            "candidate_profile"
        )


    # ------------------------------------------
    # LATEST RESUME
    # ------------------------------------------

    latest_resume = Resume.objects.filter(
        user=user
    ).order_by(
        "-uploaded_at"
    ).first()


    # ------------------------------------------
    # SKILL DETECTION
    # ------------------------------------------

    skills_list = [

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


    if latest_resume:

        resume_text = (
            latest_resume.extracted_text
            or ""
        ).lower()


        for skill in skills_list:

            if skill.lower() in resume_text:

                detected_skills.append(
                    skill
                )


    context = {

        "profile":
            profile,

        "latest_resume":
            latest_resume,

        "detected_skills":
            detected_skills,

    }


    return render(
        request,
        "accounts/candidate_profile.html",
        context
    )
# ==================================================
# ACCOUNT SETTINGS
# ==================================================

@login_required
def settings_view(request):

    user = request.user

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()

        if email:
            user.email = email
            user.save()

        password_form = PasswordChangeForm(
            user,
            request.POST
        )

        if password_form.is_valid():

            user = password_form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                "account_settings"
            )

    else:

        password_form = PasswordChangeForm(
            user
        )

    context = {
        "password_form": password_form,
        "user": user,
    }

    return render(
        request,
        "accounts/settings.html",
        context
    )