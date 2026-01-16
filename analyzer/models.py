from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('USER', 'Candidate'),
        ('HR', 'HR/Recruiter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


def resume_upload_path(instance, filename):
    return f'resumes/{instance.user.id}/{filename}'


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {os.path.basename(self.resume_file.name)}"

    class Meta:
        ordering = ['-uploaded_at']


class Job(models.Model):
    hr = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class SkillAnalysis(models.Model):
    READINESS_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('JOB_READY', 'Job Ready'),
        ('HIGHLY_COMPATIBLE', 'Highly Compatible'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    matched_skills = models.TextField()
    missing_skills = models.TextField()
    gap_percentage = models.FloatField()
    match_score = models.FloatField()
    readiness_level = models.CharField(max_length=20, choices=READINESS_CHOICES)

    analyzed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ FIX ADDED

    def __str__(self):
        return f"{self.resume.user.username} - {self.job.title} ({self.match_score}%)"

    class Meta:
        ordering = ['-analyzed_at']
        unique_together = ['resume', 'job']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']
