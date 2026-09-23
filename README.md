# HireFlow 🚀

HireFlow is a Django-based recruitment platform designed to connect job seekers and recruiters through a single web application.

The platform provides job discovery, resume analysis, job matching, application tracking, recruiter job management, and REST APIs.

## ✨ Features

### 👤 Candidate Features

- User registration and login
- Candidate dashboard
- Candidate profile management
- Resume upload
- Resume text extraction
- Resume skill detection
- Resume profile score
- Job matching
- Job browsing
- Job application
- Application status tracking
- My Applications page

### 🏢 Recruiter Features

- Recruiter registration
- Company profile
- Recruiter dashboard
- Post jobs
- Manage jobs
- Edit jobs
- Delete jobs
- View candidate applications
- Update application status

### 📄 Resume Analyzer

HireFlow allows candidates to upload resumes and process extracted resume content.

The system can detect technical skills such as:

- Python
- Java
- Django
- HTML
- CSS
- JavaScript
- MySQL
- SQL
- React
- Git
- GitHub
- REST API
- C++
- C
- Spring Boot
- MongoDB
- Node.js
- Express.js
- Bootstrap
- Docker

### 🎯 Job Matching

HireFlow compares detected resume skills with required job skills and calculates a matching result.

This helps candidates identify jobs that match their technical profile.

### 📋 Application Tracking

Candidates can:

- Apply for jobs
- View submitted applications
- Check application status

Recruiters can:

- View applications
- Update application status

Supported application statuses include:

- Applied
- Shortlisted
- Interview
- Rejected
- Selected

## 🔌 REST API

HireFlow includes REST API endpoints for jobs, applications, and resume-related functionality.

### Job APIs

```text
/api/jobs/
/api/jobs/<id>/
/api/jobs/create/