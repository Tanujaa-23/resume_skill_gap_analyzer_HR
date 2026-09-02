# Database Access Guide - SQLite Database

## Overview
This guide shows you how to view and query the SQLite database to see all uploaded resumes, jobs, and analyses.

## Method 1: Django Admin Interface (Recommended)

### Access the Admin Panel:
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: `http://localhost:8000/admin/`

3. Login with superuser credentials (create one if needed):
   ```bash
   python manage.py createsuperuser
   ```

### View Data in Admin:

#### Resumes Table:
- Go to: **Analyzer → Resumes**
- You'll see:
  - Candidate Name
  - Username
  - File Name
  - Upload Date
  - Text Extraction Status (✓/✗)
- Click any resume to view full details including extracted text

#### Jobs Table:
- Go to: **Analyzer → Jobs**
- You'll see:
  - Job Title
  - HR User
  - Skills Required (count)
  - Candidates Analyzed (count)
  - Created Date

#### Skill Analyses Table:
- Go to: **Analyzer → Skill Analyses**
- You'll see:
  - Candidate Name
  - Job Title
  - Match Score (color-coded: green ≥70%, orange ≥50%, red <50%)
  - Gap Percentage
  - Readiness Level
  - Analysis Date
- Click any analysis to see:
  - Matched Skills
  - Partially Matched Skills
  - Missing Skills

#### User Profiles Table:
- Go to: **Analyzer → User Profiles**
- See all users and their roles (Candidate/HR)

#### Notifications Table:
- Go to: **Analyzer → Notifications**
- View all notifications sent to users

## Method 2: HR Dashboard - All Resumes Page

### Access via Web Interface:
1. Login as HR user
2. Go to HR Dashboard
3. Click "All Resumes" button
4. You'll see a comprehensive table with:
   - Candidate information
   - Resume files
   - Upload dates
   - Quick analyze options
   - Search functionality

### Features:
- **Search**: Find resumes by name, email, or content
- **Pagination**: Navigate through large datasets
- **Quick Actions**: Analyze resumes directly from the table
- **Download**: Click to view/download resume files

## Method 3: SQLite Command Line

### Using SQLite3 CLI:

1. **Open the database:**
   ```bash
   sqlite3 db.sqlite3
   ```

2. **View all tables:**
   ```sql
   .tables
   ```

3. **View table structure:**
   ```sql
   .schema analyzer_resume
   .schema analyzer_job
   .schema analyzer_skillanalysis
   ```

4. **Query resumes:**
   ```sql
   -- View all resumes
   SELECT * FROM analyzer_resume;
   
   -- View resumes with user info
   SELECT 
       r.id,
       u.username,
       u.first_name,
       u.last_name,
       u.email,
       r.resume_file,
       r.uploaded_at
   FROM analyzer_resume r
   JOIN auth_user u ON r.user_id = u.id
   ORDER BY r.uploaded_at DESC;
   
   -- Count resumes per user
   SELECT 
       u.username,
       COUNT(r.id) as resume_count
   FROM analyzer_resume r
   JOIN auth_user u ON r.user_id = u.id
   GROUP BY u.username;
   ```

5. **Query jobs:**
   ```sql
   -- View all jobs
   SELECT * FROM analyzer_job;
   
   -- View jobs with HR info
   SELECT 
       j.id,
       j.title,
       u.username as hr_username,
       j.required_skills,
       j.created_at
   FROM analyzer_job j
   JOIN auth_user u ON j.hr_id = u.id
   ORDER BY j.created_at DESC;
   ```

6. **Query skill analyses:**
   ```sql
   -- View all analyses
   SELECT * FROM analyzer_skillanalysis;
   
   -- View detailed analysis results
   SELECT 
       u.username as candidate,
       j.title as job_title,
       sa.match_score,
       sa.gap_percentage,
       sa.readiness_level,
       sa.analyzed_at
   FROM analyzer_skillanalysis sa
   JOIN analyzer_resume r ON sa.resume_id = r.id
   JOIN auth_user u ON r.user_id = u.id
   JOIN analyzer_job j ON sa.job_id = j.id
   ORDER BY sa.match_score DESC;
   
   -- Find top candidates for a specific job
   SELECT 
       u.username,
       u.first_name,
       u.last_name,
       sa.match_score,
       sa.readiness_level
   FROM analyzer_skillanalysis sa
   JOIN analyzer_resume r ON sa.resume_id = r.id
   JOIN auth_user u ON r.user_id = u.id
   WHERE sa.job_id = 1  -- Replace with your job ID
   ORDER BY sa.match_score DESC
   LIMIT 10;
   ```

7. **Useful queries:**
   ```sql
   -- Count total resumes
   SELECT COUNT(*) as total_resumes FROM analyzer_resume;
   
   -- Count total jobs
   SELECT COUNT(*) as total_jobs FROM analyzer_job;
   
   -- Count total analyses
   SELECT COUNT(*) as total_analyses FROM analyzer_skillanalysis;
   
   -- Average match score
   SELECT AVG(match_score) as avg_match_score 
   FROM analyzer_skillanalysis;
   
   -- Resumes without analyses
   SELECT 
       u.username,
       r.uploaded_at
   FROM analyzer_resume r
   JOIN auth_user u ON r.user_id = u.id
   LEFT JOIN analyzer_skillanalysis sa ON r.id = sa.resume_id
   WHERE sa.id IS NULL;
   
   -- Jobs with most candidates
   SELECT 
       j.title,
       COUNT(sa.id) as candidate_count
   FROM analyzer_job j
   LEFT JOIN analyzer_skillanalysis sa ON j.id = sa.job_id
   GROUP BY j.id
   ORDER BY candidate_count DESC;
   ```

8. **Export data to CSV:**
   ```sql
   .mode csv
   .output resumes.csv
   SELECT * FROM analyzer_resume;
   .output stdout
   ```

9. **Exit SQLite:**
   ```sql
   .quit
   ```

## Method 4: Python Django Shell

### Using Django ORM:

1. **Open Django shell:**
   ```bash
   python manage.py shell
   ```

2. **Import models:**
   ```python
   from analyzer.models import Resume, Job, SkillAnalysis, UserProfile
   from django.contrib.auth.models import User
   ```

3. **Query resumes:**
   ```python
   # Get all resumes
   resumes = Resume.objects.all()
   for resume in resumes:
       print(f"{resume.user.username}: {resume.resume_file.name}")
   
   # Get resumes with extracted text
   resumes_with_text = Resume.objects.exclude(extracted_text='')
   print(f"Resumes with extracted text: {resumes_with_text.count()}")
   
   # Get latest resume
   latest = Resume.objects.latest('uploaded_at')
   print(f"Latest resume: {latest.user.username} - {latest.uploaded_at}")
   ```

4. **Query jobs:**
   ```python
   # Get all jobs
   jobs = Job.objects.all()
   for job in jobs:
       print(f"{job.title} by {job.hr.username}")
   
   # Get jobs with analyses count
   for job in Job.objects.all():
       count = job.analyses.count()
       print(f"{job.title}: {count} candidates")
   ```

5. **Query analyses:**
   ```python
   # Get all analyses
   analyses = SkillAnalysis.objects.all()
   
   # Get top matches
   top_matches = SkillAnalysis.objects.filter(
       match_score__gte=80
   ).order_by('-match_score')
   
   for analysis in top_matches:
       print(f"{analysis.resume.user.username}: {analysis.match_score}%")
   
   # Get analyses for specific job
   job = Job.objects.first()
   job_analyses = SkillAnalysis.objects.filter(job=job)
   ```

6. **Statistics:**
   ```python
   from django.db.models import Avg, Count
   
   # Average match score
   avg_score = SkillAnalysis.objects.aggregate(Avg('match_score'))
   print(f"Average match score: {avg_score['match_score__avg']:.2f}%")
   
   # Count by readiness level
   readiness_counts = SkillAnalysis.objects.values('readiness_level').annotate(
       count=Count('id')
   )
   for item in readiness_counts:
       print(f"{item['readiness_level']}: {item['count']}")
   ```

## Method 5: Database Browser Tools

### Using DB Browser for SQLite (GUI Tool):

1. **Download and install:**
   - Visit: https://sqlitebrowser.org/
   - Download for your OS
   - Install the application

2. **Open database:**
   - Launch DB Browser for SQLite
   - Click "Open Database"
   - Navigate to your project folder
   - Select `db.sqlite3`

3. **Browse data:**
   - Click "Browse Data" tab
   - Select table from dropdown
   - View all records in table format
   - Sort, filter, and search data

4. **Execute SQL:**
   - Click "Execute SQL" tab
   - Write custom queries
   - View results in table format

## Database Tables Reference

### Main Tables:

1. **analyzer_resume**
   - id: Primary key
   - user_id: Foreign key to auth_user
   - resume_file: File path
   - extracted_text: Extracted resume text
   - uploaded_at: Timestamp

2. **analyzer_job**
   - id: Primary key
   - hr_id: Foreign key to auth_user
   - title: Job title
   - description: Job description
   - required_skills: Comma-separated skills
   - created_at: Timestamp

3. **analyzer_skillanalysis**
   - id: Primary key
   - resume_id: Foreign key to analyzer_resume
   - job_id: Foreign key to analyzer_job
   - matched_skills: Comma-separated matched skills
   - partially_matched_skills: Comma-separated partial matches
   - missing_skills: Comma-separated missing skills
   - match_score: Float (0-100)
   - gap_percentage: Float (0-100)
   - readiness_level: Choice field
   - analyzed_at: Timestamp
   - updated_at: Timestamp

4. **analyzer_userprofile**
   - id: Primary key
   - user_id: Foreign key to auth_user
   - role: USER or HR
   - created_at: Timestamp

5. **analyzer_notification**
   - id: Primary key
   - user_id: Foreign key to auth_user
   - message: Text
   - is_read: Boolean
   - created_at: Timestamp

## Quick Reference Commands

```bash
# Create superuser for admin access
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Open database shell
python manage.py dbshell

# Create database backup
sqlite3 db.sqlite3 ".backup backup.db"

# Restore database from backup
sqlite3 db.sqlite3 ".restore backup.db"
```

## Tips

1. **Best Method**: Use Django Admin for most tasks - it's user-friendly and shows formatted data
2. **For HR Users**: Use the "All Resumes" page for quick access to resume data
3. **For Developers**: Use Django shell for complex queries and data manipulation
4. **For Reports**: Use SQLite CLI to export data to CSV
5. **For Visualization**: Use DB Browser for SQLite for a GUI experience

## Troubleshooting

**Issue**: Can't access admin panel
- **Solution**: Create superuser with `python manage.py createsuperuser`

**Issue**: Database locked error
- **Solution**: Close all connections to the database, stop the dev server

**Issue**: No data showing
- **Solution**: Ensure migrations are applied with `python manage.py migrate`

**Issue**: Permission denied
- **Solution**: Check file permissions on db.sqlite3

## Security Note

The SQLite database file (`db.sqlite3`) contains sensitive information. In production:
- Never commit it to version control
- Use proper database backups
- Consider using PostgreSQL or MySQL for production
- Implement proper access controls
