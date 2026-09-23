from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pypdf import PdfReader

from .models import Resume


# Skills that HireFlow can detect
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


# Calculate Resume Score
def calculate_resume_score(text, detected_skills):

    text_lower = text.lower()

    # --------------------------------
    # 1. Technical Skills - 30 Marks
    # --------------------------------
    skill_score = min(len(detected_skills) * 3, 30)


    # --------------------------------
    # 2. Projects - 25 Marks
    # --------------------------------
    project_keywords = [
        "project",
        "projects",
        "developed",
        "application",
        "system"
    ]

    project_found = sum(
        1
        for keyword in project_keywords
        if keyword in text_lower
    )

    project_score = min(project_found * 5, 25)


    # --------------------------------
    # 3. Education - 20 Marks
    # --------------------------------
    education_keywords = [
        "education",
        "academic",
        "university",
        "college",
        "degree",
        "mca",
        "bachelor"
    ]

    education_found = sum(
        1
        for keyword in education_keywords
        if keyword in text_lower
    )

    education_score = min(education_found * 3, 20)


    # --------------------------------
    # 4. Experience - 15 Marks
    # --------------------------------
    experience_keywords = [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "intern"
    ]

    experience_found = any(
        keyword in text_lower
        for keyword in experience_keywords
    )

    if experience_found:
        experience_score = 15
    else:
        experience_score = 0


    # --------------------------------
    # 5. Certifications - 10 Marks
    # --------------------------------
    certification_keywords = [
        "certification",
        "certified",
        "certificate",
        "coursera",
        "udemy"
    ]

    certification_found = any(
        keyword in text_lower
        for keyword in certification_keywords
    )

    if certification_found:
        certification_score = 10
    else:
        certification_score = 0


    # --------------------------------
    # Total Score
    # --------------------------------
    total_score = (
        skill_score
        + project_score
        + education_score
        + experience_score
        + certification_score
    )


    # --------------------------------
    # Return Complete Score Data
    # --------------------------------
    return {
        "total": min(total_score, 100),
        "skills": skill_score,
        "projects": project_score,
        "education": education_score,
        "experience": experience_score,
        "certifications": certification_score,
    }


# Resume Upload View
@login_required
def resume_upload(request):

    if request.method == "POST":

        uploaded_file = request.FILES.get("resume")


        # --------------------------------
        # Check File
        # --------------------------------
        if not uploaded_file:

            return render(
                request,
                "resume_analyzer/upload.html",
                {
                    "error": "Please select a PDF resume."
                }
            )


        # --------------------------------
        # Check PDF
        # --------------------------------
        if not uploaded_file.name.lower().endswith(".pdf"):

            return render(
                request,
                "resume_analyzer/upload.html",
                {
                    "error": "Only PDF files are allowed."
                }
            )


        # --------------------------------
        # Check File Size
        # --------------------------------
        if uploaded_file.size > 5 * 1024 * 1024:

            return render(
                request,
                "resume_analyzer/upload.html",
                {
                    "error": "File size must be less than 5 MB."
                }
            )


        try:

            # --------------------------------
            # Save Uploaded File
            # --------------------------------
            file_path = default_storage.save(
                f"resumes/{uploaded_file.name}",
                ContentFile(uploaded_file.read())
            )


            # --------------------------------
            # Get Full File Path
            # --------------------------------
            full_path = default_storage.path(file_path)


            # --------------------------------
            # Read PDF
            # --------------------------------
            reader = PdfReader(full_path)


            extracted_text = ""


            for page in reader.pages:

                text = page.extract_text()

                if text:

                    extracted_text += text + "\n"


            # --------------------------------
            # Detect Skills
            # --------------------------------
            resume_text = extracted_text.lower()

            detected_skills = []


            for skill in SKILLS:

                if skill.lower() in resume_text:

                    detected_skills.append(skill)


            # --------------------------------
            # Calculate Score
            # --------------------------------
            score_data = calculate_resume_score(
                extracted_text,
                detected_skills
            )


            # --------------------------------
            # Get Total Score
            # --------------------------------
            resume_score = score_data["total"]


            # --------------------------------
            # Save Resume in Database
            # --------------------------------
            resume = Resume.objects.create(
                user=request.user,
                resume_file=file_path,
                extracted_text=extracted_text
            )


            # --------------------------------
            # Show Result Page
            # --------------------------------
            return render(
                request,
                "resume_analyzer/result.html",
                {
                    "resume": resume,
                    "detected_skills": detected_skills,
                    "resume_score": resume_score,
                    "score_data": score_data,
                }
            )


        except Exception as e:

            return render(
                request,
                "resume_analyzer/upload.html",
                {
                    "error": f"Could not process the PDF: {e}"
                }
            )


    # --------------------------------
    # GET Request
    # --------------------------------
    return render(
        request,
        "resume_analyzer/upload.html"
    )