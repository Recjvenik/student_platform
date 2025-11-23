from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import StudentProfile, Experience


class ExperienceInline(admin.TabularInline):
    """Inline admin for experiences"""
    model = Experience
    extra = 1


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Student Profile admin with CSV export"""
    
    list_display = ['full_name', 'user_email', 'user_mobile', 'college_name', 'graduation_year', 
                    'step_completed', 'is_complete', 'created_at']
    list_filter = ['is_complete', 'graduation_year', 'work_type', 'current_status', 'created_at']
    search_fields = ['full_name', 'user__email', 'user__mobile', 'college_name', 'university']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at']
    ordering = ['-created_at']
    
    inlines = [ExperienceInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Basic Details', {
            'fields': ('full_name', 'gender', 'date_of_birth', 'current_city', 'current_state', 
                      'preferred_languages')
        }),
        ('Education', {
            'fields': ('current_status', 'highest_qualification', 'stream_specialization', 
                      'college_name', 'university', 'graduation_year', 'academic_scores', 
                      'has_backlogs', 'num_backlogs')
        }),
        ('Skills', {
            'fields': ('english_speaking', 'english_reading', 'english_writing', 
                      'computer_skills', 'tool_exposure', 'typing_speed')
        }),
        ('Career Preferences', {
            'fields': ('preferred_job_roles', 'preferred_industries', 'work_type', 
                      'preferred_locations', 'willing_to_relocate', 'expected_salary')
        }),
        ('Availability', {
            'fields': ('time_for_training', 'preferred_time_slots', 'has_mobile_access', 
                      'has_laptop_access', 'internet_quality', 'constraints')
        }),
        ('Behavioural Fit', {
            'fields': ('comfort_talking_strangers', 'comfort_handling_angry_customers', 
                      'comfort_working_with_data', 'comfort_following_targets', 
                      'comfort_writing_emails', 'people_vs_task_oriented', 'office_vs_remote', 
                      'analysis_vs_communication', 'career_concerns', 'career_goal_3_years')
        }),
        ('Training Information', {
            'fields': ('previous_training', 'discovery_source', 'commitment_confirmed', 
                      'fee_preference')
        }),
        ('Documents', {
            'fields': ('photo', 'resume', 'id_proof', 'marksheet')
        }),
        ('Progress', {
            'fields': ('step_completed', 'is_complete', 'submitted_at', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['export_as_csv']
    
    def user_email(self, obj):
        return obj.user.email or '-'
    user_email.short_description = 'Email'
    
    def user_mobile(self, obj):
        return obj.user.mobile or '-'
    user_mobile.short_description = 'Mobile'
    
    def export_as_csv(self, request, queryset):
        """Export selected student profiles as CSV"""
        
        meta = self.model._meta
        field_names = [
            'full_name', 'gender', 'date_of_birth', 'current_city', 'current_state',
            'current_status', 'highest_qualification', 'college_name', 'university',
            'graduation_year', 'academic_scores', 'preferred_job_roles', 'expected_salary',
            'work_type', 'willing_to_relocate', 'typing_speed', 'is_complete'
        ]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=student_profiles.csv'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Mobile'] + field_names)
        
        for obj in queryset:
            row = [obj.user.email or '', obj.user.mobile or '']
            for field in field_names:
                value = getattr(obj, field)
                if isinstance(value, list):
                    value = ', '.join(map(str, value))
                row.append(value)
            writer.writerow(row)
        
        return response
    
    export_as_csv.short_description = 'Export Selected as CSV'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Experience admin"""
    
    list_display = ['student_name', 'company_name', 'role', 'duration', 'created_at']
    list_filter = ['created_at']
    search_fields = ['company_name', 'role', 'student_profile__full_name']
    ordering = ['-created_at']
    
    def student_name(self, obj):
        return obj.student_profile.full_name
    student_name.short_description = 'Student'