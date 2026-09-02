from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Resume, Job, SkillAnalysis, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    date_hierarchy = 'created_at'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['get_candidate_name', 'user', 'get_file_name', 'uploaded_at', 'has_extracted_text']
    list_filter = ['uploaded_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'extracted_text']
    readonly_fields = ['extracted_text', 'uploaded_at']
    date_hierarchy = 'uploaded_at'
    
    def get_candidate_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_candidate_name.short_description = 'Candidate Name'
    
    def get_file_name(self, obj):
        import os
        return os.path.basename(obj.resume_file.name)
    get_file_name.short_description = 'File Name'
    
    def has_extracted_text(self, obj):
        if obj.extracted_text:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    has_extracted_text.short_description = 'Text Extracted'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'hr', 'get_required_skills_count', 'get_candidates_count', 'created_at']
    list_filter = ['created_at', 'hr']
    search_fields = ['title', 'description', 'required_skills', 'hr__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_required_skills_count(self, obj):
        skills = [s.strip() for s in obj.required_skills.split(',') if s.strip()]
        return len(skills)
    get_required_skills_count.short_description = 'Skills Required'
    
    def get_candidates_count(self, obj):
        return obj.analyses.count()
    get_candidates_count.short_description = 'Candidates Analyzed'


@admin.register(SkillAnalysis)
class SkillAnalysisAdmin(admin.ModelAdmin):
    list_display = ['get_candidate_name', 'job', 'match_score_display', 'gap_percentage_display', 
                    'readiness_level', 'analyzed_at']
    list_filter = ['readiness_level', 'analyzed_at', 'job']
    search_fields = ['resume__user__username', 'resume__user__first_name', 'resume__user__last_name', 
                     'job__title']
    readonly_fields = ['matched_skills', 'partially_matched_skills', 'missing_skills', 
                       'analyzed_at', 'updated_at']
    date_hierarchy = 'analyzed_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('resume', 'job', 'readiness_level')
        }),
        ('Analysis Results', {
            'fields': ('match_score', 'gap_percentage', 'matched_skills', 
                      'partially_matched_skills', 'missing_skills')
        }),
        ('Timestamps', {
            'fields': ('analyzed_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_candidate_name(self, obj):
        return obj.resume.user.get_full_name() or obj.resume.user.username
    get_candidate_name.short_description = 'Candidate'
    
    def match_score_display(self, obj):
        color = 'green' if obj.match_score >= 70 else 'orange' if obj.match_score >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, obj.match_score
        )
    match_score_display.short_description = 'Match Score'
    
    def gap_percentage_display(self, obj):
        color = 'red' if obj.gap_percentage >= 50 else 'orange' if obj.gap_percentage >= 30 else 'green'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, obj.gap_percentage
        )
    gap_percentage_display.short_description = 'Gap %'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'message']
    date_hierarchy = 'created_at'
    
    def get_message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    get_message_preview.short_description = 'Message'