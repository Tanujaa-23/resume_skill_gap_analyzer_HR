# Database Structure - Resume Skill Gap Analyzer

## Database Overview

The application uses SQLite database (`db.sqlite3`) with the following main tables:

## Table Relationships

```
auth_user (Django built-in)
    ↓
    ├─→ analyzer_userprofile (1:1)
    ├─→ analyzer_resume (1:Many)
    ├─→ analyzer_job (1:Many) [HR users only]
    └─→ analyzer_notification (1:Many)

analyzer_resume
    ↓
    └─→ analyzer_skillanalysis (1:Many)

analyzer_job
    ↓
    └─→ analyzer_skillanalysis (1:Many)
```

## Detailed Table Structures

### 1. auth_user (Django Built-in)
Standard Django user table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| username | VARCHAR(150) | Unique username |
| first_name | VARCHAR(150) | First name |
| last_name | VARCHAR(150) | Last name |
| email | VARCHAR(254) | Email address |
| password | VARCHAR(128) | Hashed password |
| is_staff | BOOLEAN | Admin access |
| is_active | BOOLEAN | Account status |
| date_joined | DATETIME | Registration date |

**Sample Query:**
```sql
SELECT id, username, first_name, last_name, email, date_joined 
FROM auth_user;
```

---

### 2. analyzer_userprofile
User role information (Candidate or HR)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key → auth_user.id |
| role | VARCHAR(10) | 'USER' or 'HR' |
| created_at | DATETIME | Profile creation date |

**Sample Query:**
```sql
SELECT 
    up.id,
    u.username,
    u.email,
    up.role,
    up.created_at
FROM analyzer_userprofile up
JOIN auth_user u ON up.user_id = u.id;
```

**View in Admin:** `/admin/analyzer/userprofile/`

---

### 3. analyzer_resume
Uploaded resume files and extracted text

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key → auth_user.id |
| resume_file | VARCHAR(100) | File path (media/resumes/...) |
| extracted_text | TEXT | Extracted resume text |
| uploaded_at | DATETIME | Upload timestamp |

**Sample Query:**
```sql
SELECT 
    r.id,
    u.username,
    u.first_name || ' ' || u.last_name as full_name,
    u.email,
    r.resume_file,
    r.uploaded_at,
    CASE 
        WHEN r.extracted_text != '' THEN 'Yes'
        ELSE 'No'
    END as text_extracted
FROM analyzer_resume r
JOIN auth_user u ON r.user_id = u.id
ORDER BY r.uploaded_at DESC;
```

**View in Admin:** `/admin/analyzer/resume/`

**View in HR Dashboard:** `/all-resumes/`

---

### 4. analyzer_job
Job postings created by HR users

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| hr_id | INTEGER | Foreign Key → auth_user.id |
| title | VARCHAR(200) | Job title |
| description | TEXT | Job description |
| required_skills | TEXT | Comma-separated skills |
| created_at | DATETIME | Job creation date |

**Sample Query:**
```sql
SELECT 
    j.id,
    j.title,
    u.username as hr_username,
    j.required_skills,
    j.created_at,
    (SELECT COUNT(*) 
     FROM analyzer_skillanalysis sa 
     WHERE sa.job_id = j.id) as candidates_analyzed
FROM analyzer_job j
JOIN auth_user u ON j.hr_id = u.id
ORDER BY j.created_at DESC;
```

**View in Admin:** `/admin/analyzer/job/`

---

### 5. analyzer_skillanalysis ⭐ (Main Analysis Table)
Analysis results comparing resumes to jobs

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| resume_id | INTEGER | Foreign Key → analyzer_resume.id |
| job_id | INTEGER | Foreign Key → analyzer_job.id |
| matched_skills | TEXT | Comma-separated exact matches |
| partially_matched_skills | TEXT | Comma-separated partial matches ⭐ NEW |
| missing_skills | TEXT | Comma-separated missing skills |
| match_score | REAL | Match percentage (0-100) |
| gap_percentage | REAL | Gap percentage (0-100) |
| readiness_level | VARCHAR(20) | BEGINNER/INTERMEDIATE/JOB_READY/HIGHLY_COMPATIBLE |
| analyzed_at | DATETIME | Analysis timestamp |
| updated_at | DATETIME | Last update timestamp ⭐ NEW |

**Sample Query:**
```sql
SELECT 
    sa.id,
    u.username as candidate,
    u.first_name || ' ' || u.last_name as candidate_name,
    j.title as job_title,
    sa.match_score,
    sa.gap_percentage,
    sa.readiness_level,
    sa.matched_skills,
    sa.partially_matched_skills,
    sa.missing_skills,
    sa.analyzed_at
FROM analyzer_skillanalysis sa
JOIN analyzer_resume r ON sa.resume_id = r.id
JOIN auth_user u ON r.user_id = u.id
JOIN analyzer_job j ON sa.job_id = j.id
ORDER BY sa.match_score DESC;
```

**View in Admin:** `/admin/analyzer/skillanalysis/`

---

### 6. analyzer_notification
Notifications sent to users

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key → auth_user.id |
| message | TEXT | Notification message |
| is_read | BOOLEAN | Read status |
| created_at | DATETIME | Notification timestamp |

**Sample Query:**
```sql
SELECT 
    n.id,
    u.username,
    n.message,
    n.is_read,
    n.created_at
FROM analyzer_notification n
JOIN auth_user u ON n.user_id = u.id
ORDER BY n.created_at DESC;
```

**View in Admin:** `/admin/analyzer/notification/`

---

## Useful SQL Queries

### Get Complete Resume Analysis
```sql
SELECT 
    u.username,
    u.first_name,
    u.last_name,
    u.email,
    r.resume_file,
    r.uploaded_at,
    j.title as job_title,
    sa.match_score,
    sa.gap_percentage,
    sa.readiness_level,
    sa.matched_skills,
    sa.partially_matched_skills,
    sa.missing_skills
FROM analyzer_skillanalysis sa
JOIN analyzer_resume r ON sa.resume_id = r.id
JOIN auth_user u ON r.user_id = u.id
JOIN analyzer_job j ON sa.job_id = j.id
WHERE sa.match_score >= 70
ORDER BY sa.match_score DESC;
```

### Find Top Candidates for Each Job
```sql
SELECT 
    j.title as job_title,
    u.username as candidate,
    sa.match_score,
    sa.readiness_level
FROM analyzer_skillanalysis sa
JOIN analyzer_resume r ON sa.resume_id = r.id
JOIN auth_user u ON r.user_id = u.id
JOIN analyzer_job j ON sa.job_id = j.id
WHERE sa.id IN (
    SELECT id 
    FROM analyzer_skillanalysis sa2
    WHERE sa2.job_id = sa.job_id
    ORDER BY sa2.match_score DESC
    LIMIT 5
)
ORDER BY j.title, sa.match_score DESC;
```

### Get Statistics by Job
```sql
SELECT 
    j.title,
    COUNT(sa.id) as total_candidates,
    AVG(sa.match_score) as avg_match_score,
    MAX(sa.match_score) as best_match,
    MIN(sa.match_score) as worst_match
FROM analyzer_job j
LEFT JOIN analyzer_skillanalysis sa ON j.id = sa.job_id
GROUP BY j.id
ORDER BY avg_match_score DESC;
```

### Find Resumes Without Analysis
```sql
SELECT 
    u.username,
    u.email,
    r.resume_file,
    r.uploaded_at
FROM analyzer_resume r
JOIN auth_user u ON r.user_id = u.id
LEFT JOIN analyzer_skillanalysis sa ON r.id = sa.resume_id
WHERE sa.id IS NULL
ORDER BY r.uploaded_at DESC;
```

### Get Most Common Missing Skills
```sql
-- Note: This requires extracting skills from comma-separated text
-- Best done in Python/Django ORM
SELECT 
    missing_skills,
    COUNT(*) as frequency
FROM analyzer_skillanalysis
WHERE missing_skills != ''
GROUP BY missing_skills
ORDER BY frequency DESC
LIMIT 10;
```

### Find Candidates by Skill
```sql
SELECT 
    u.username,
    u.email,
    r.resume_file
FROM analyzer_resume r
JOIN auth_user u ON r.user_id = u.id
WHERE r.extracted_text LIKE '%Python%'
   OR r.extracted_text LIKE '%Django%'
ORDER BY r.uploaded_at DESC;
```

## Database Statistics Queries

### Overall Statistics
```sql
SELECT 
    (SELECT COUNT(*) FROM auth_user) as total_users,
    (SELECT COUNT(*) FROM analyzer_userprofile WHERE role='HR') as hr_users,
    (SELECT COUNT(*) FROM analyzer_userprofile WHERE role='USER') as candidates,
    (SELECT COUNT(*) FROM analyzer_resume) as total_resumes,
    (SELECT COUNT(*) FROM analyzer_job) as total_jobs,
    (SELECT COUNT(*) FROM analyzer_skillanalysis) as total_analyses,
    (SELECT AVG(match_score) FROM analyzer_skillanalysis) as avg_match_score;
```

### Readiness Level Distribution
```sql
SELECT 
    readiness_level,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM analyzer_skillanalysis), 2) as percentage
FROM analyzer_skillanalysis
GROUP BY readiness_level
ORDER BY count DESC;
```

### Recent Activity
```sql
SELECT 
    'Resume Upload' as activity_type,
    u.username,
    r.uploaded_at as timestamp
FROM analyzer_resume r
JOIN auth_user u ON r.user_id = u.id
UNION ALL
SELECT 
    'Job Created' as activity_type,
    u.username,
    j.created_at as timestamp
FROM analyzer_job j
JOIN auth_user u ON j.hr_id = u.id
UNION ALL
SELECT 
    'Analysis Done' as activity_type,
    u.username,
    sa.analyzed_at as timestamp
FROM analyzer_skillanalysis sa
JOIN analyzer_resume r ON sa.resume_id = r.id
JOIN auth_user u ON r.user_id = u.id
ORDER BY timestamp DESC
LIMIT 20;
```

## Accessing the Database

### Method 1: SQLite Command Line
```bash
# Open database
sqlite3 db.sqlite3

# Enable column headers
.headers on

# Enable column mode
.mode column

# Run queries
SELECT * FROM analyzer_resume LIMIT 5;

# Exit
.quit
```

### Method 2: Django Shell
```python
# Open shell
python manage.py shell

# Import models
from analyzer.models import Resume, Job, SkillAnalysis
from django.contrib.auth.models import User

# Query examples
resumes = Resume.objects.all()
jobs = Job.objects.all()
analyses = SkillAnalysis.objects.filter(match_score__gte=70)

# Get statistics
from django.db.models import Avg, Count
avg_score = SkillAnalysis.objects.aggregate(Avg('match_score'))
```

### Method 3: Django Admin
```
URL: http://localhost:8000/admin/
- Visual interface
- Color-coded results
- Search and filter
- Export capabilities
```

### Method 4: HR Dashboard
```
URL: http://localhost:8000/all-resumes/
- Table view of all resumes
- Search functionality
- Quick analyze
- Statistics
```

## Database Backup and Restore

### Create Backup
```bash
# Using SQLite
sqlite3 db.sqlite3 ".backup backup_$(date +%Y%m%d).db"

# Or simple copy
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

### Restore Backup
```bash
# Using SQLite
sqlite3 db.sqlite3 ".restore backup.db"

# Or simple copy
cp backup.db db.sqlite3
```

## Database Maintenance

### Check Database Integrity
```bash
sqlite3 db.sqlite3 "PRAGMA integrity_check;"
```

### Optimize Database
```bash
sqlite3 db.sqlite3 "VACUUM;"
```

### View Database Size
```bash
# Windows
dir db.sqlite3

# Linux/Mac
ls -lh db.sqlite3
```

## Important Notes

1. **Primary Keys**: All tables use auto-incrementing INTEGER primary keys
2. **Foreign Keys**: Properly set up with ON DELETE CASCADE where appropriate
3. **Indexes**: Django automatically creates indexes on foreign keys
4. **Timestamps**: All timestamps are in UTC
5. **Text Fields**: Use TEXT type for unlimited length
6. **Unique Constraints**: (resume_id, job_id) is unique in skillanalysis table

## Security Considerations

1. **Passwords**: Stored as hashed values in auth_user table
2. **File Paths**: Resume files stored in media/resumes/ directory
3. **Access Control**: Views check user permissions before allowing access
4. **SQL Injection**: Django ORM prevents SQL injection attacks
5. **Backup**: Regular backups recommended for production

## Performance Tips

1. **Indexes**: Consider adding indexes on frequently queried fields
2. **Pagination**: Use pagination for large result sets
3. **Select Related**: Use select_related() for foreign key queries
4. **Prefetch Related**: Use prefetch_related() for reverse foreign keys
5. **Database Optimization**: Run VACUUM periodically

## Conclusion

This database structure provides:
- ✅ Complete user management
- ✅ Resume storage and tracking
- ✅ Job posting management
- ✅ Detailed skill analysis
- ✅ Notification system
- ✅ Easy querying and reporting
- ✅ Scalable design

For more information, see:
- DATABASE_ACCESS_GUIDE.md
- QUICK_START_GUIDE.md
- IMPROVEMENTS.md
