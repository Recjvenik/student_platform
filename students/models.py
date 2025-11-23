from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    """Comprehensive student profile with all registration data"""
    
    # Relationship to User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # SECTION A - Basic Information
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')
    ])
    date_of_birth = models.DateField()
    current_city = models.CharField(max_length=100)
    current_state = models.CharField(max_length=100)
    preferred_languages = models.JSONField(default=list, help_text='List of preferred languages')
    
    # SECTION B - Education Details
    current_status = models.CharField(max_length=50, choices=[
        ('student', 'Student'), ('graduate', 'Graduate'), ('postgraduate', 'Postgraduate')
    ])
    highest_qualification = models.CharField(max_length=100)
    stream_specialization = models.CharField(max_length=100)
    college_name = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    graduation_year = models.IntegerField()
    academic_scores = models.CharField(max_length=50, help_text='CGPA/Percentage')
    has_backlogs = models.BooleanField(default=False)
    num_backlogs = models.IntegerField(default=0)
    
    # SECTION C - Skills & Exposure
    english_speaking = models.IntegerField(default=1, help_text='1-5 rating')
    english_reading = models.IntegerField(default=1, help_text='1-5 rating')
    english_writing = models.IntegerField(default=1, help_text='1-5 rating')
    computer_skills = models.JSONField(default=list, help_text='List of computer skills')
    tool_exposure = models.JSONField(default=list, help_text='List of tools known')
    typing_speed = models.IntegerField(default=0, help_text='WPM')
    
    # SECTION D - Career Preferences
    preferred_job_roles = models.JSONField(default=list, help_text='Priority-ranked list of job roles')
    preferred_industries = models.JSONField(default=list, help_text='List of preferred industries')
    work_type = models.CharField(max_length=20, choices=[
        ('remote', 'Remote'), ('office', 'Office'), ('hybrid', 'Hybrid'), ('any', 'Any')
    ])
    preferred_locations = models.JSONField(default=list, help_text='List of preferred work locations')
    willing_to_relocate = models.BooleanField(default=False)
    expected_salary = models.CharField(max_length=50)
    
    # SECTION E - Availability & Constraints
    time_for_training = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'), ('part_time', 'Part Time'), ('weekends', 'Weekends Only')
    ])
    preferred_time_slots = models.JSONField(default=list, help_text='Preferred training time slots')
    has_mobile_access = models.BooleanField(default=True)
    has_laptop_access = models.BooleanField(default=False)
    internet_quality = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')
    ])
    constraints = models.TextField(blank=True, help_text='Any constraints or limitations')
    
    # SECTION F - Behavioural Fit (Likert scales 1-5)
    comfort_talking_strangers = models.IntegerField(default=3)
    comfort_handling_angry_customers = models.IntegerField(default=3)
    comfort_working_with_data = models.IntegerField(default=3)
    comfort_following_targets = models.IntegerField(default=3)
    comfort_writing_emails = models.IntegerField(default=3)
    
    # Binary behavioral preferences
    people_vs_task_oriented = models.CharField(max_length=20, choices=[
        ('people', 'People-oriented'), ('task', 'Task-oriented')
    ])
    office_vs_remote = models.CharField(max_length=20, choices=[
        ('office', 'Office'), ('remote', 'Remote')
    ])
    analysis_vs_communication = models.CharField(max_length=20, choices=[
        ('analysis', 'Analysis'), ('communication', 'Communication')
    ])
    
    career_concerns = models.JSONField(default=list, help_text='List of career concerns')
    career_goal_3_years = models.TextField(help_text='Career goal in 3 years (3-4 lines)')
    
    # SECTION G - Training Program Information
    previous_training = models.TextField(blank=True, help_text='Details of previous training')
    discovery_source = models.CharField(max_length=100, help_text='How did you find us')
    commitment_confirmed = models.BooleanField(default=False)
    fee_preference = models.CharField(max_length=50, choices=[
        ('upfront', 'Pay Upfront'), ('emi', 'EMI'), ('free', 'Free Program'), ('scholarship', 'Scholarship')
    ])
    
    # SECTION H - Document Uploads
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    marksheet = models.FileField(upload_to='marksheets/', blank=True, null=True)
    
    # Progress Tracking
    step_completed = models.IntegerField(default=0, help_text='Last completed step (0-8)')
    is_complete = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f'{self.full_name} - {self.user.email or self.user.mobile}'
    
    def get_progress_percentage(self):
        """Calculate completion percentage"""
        return int((self.step_completed / 8) * 100)


class Experience(models.Model):
    """Model for student work experience/internships"""
    
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    duration = models.CharField(max_length=100, help_text='e.g., 6 months, 1 year')
    description = models.TextField(help_text='Brief description of responsibilities')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'experiences'
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.role} at {self.company_name}'