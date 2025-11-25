from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from .models import StudentProfile, Experience


class Step1BasicInfoForm(forms.ModelForm):
    """Step 1: Basic Information Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'gender', 'date_of_birth', 'current_city', 
                  'current_state', 'preferred_languages']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'id': 'full_name'
            }),
            'gender': forms.RadioSelect(attrs={
                'class': 'radio-input'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date_of_birth',
                'max': date.today().isoformat()
            }),
            'current_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mumbai, Delhi, Bangalore',
                'id': 'current_city'
            }),
            'current_state': forms.Select(attrs={
                'class': 'form-control',
                'id': 'current_state'
            }),
        }
    
    # Preferred languages as multiple checkboxes
    lang_english = forms.BooleanField(required=False, label='English')
    lang_hindi = forms.BooleanField(required=False, label='Hindi')
    lang_tamil = forms.BooleanField(required=False, label='Tamil')
    lang_telugu = forms.BooleanField(required=False, label='Telugu')
    lang_kannada = forms.BooleanField(required=False, label='Kannada')
    lang_bengali = forms.BooleanField(required=False, label='Bengali')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        self.fields['full_name'].required = True
        self.fields['gender'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['current_city'].required = True
        self.fields['current_state'].required = True
        
        # Pre-populate language checkboxes if editing
        if self.instance and self.instance.pk and self.instance.preferred_languages:
            for lang in self.instance.preferred_languages:
                field_name = f'lang_{lang.lower()}'
                if field_name in self.fields:
                    self.initial[field_name] = True
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if len(full_name) < 3:
            raise ValidationError('Full name must be at least 3 characters long')
        return full_name
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            # Check if user is at least 16 years old
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 16:
                raise ValidationError('You must be at least 16 years old')
            if dob > today:
                raise ValidationError('Date of birth cannot be in the future')
        return dob
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect selected languages
        languages = []
        for lang in ['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Bengali']:
            if cleaned_data.get(f'lang_{lang.lower()}'):
                languages.append(lang)
        
        if not languages:
            raise ValidationError('Please select at least one preferred language')
        
        cleaned_data['preferred_languages'] = languages
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.preferred_languages = self.cleaned_data.get('preferred_languages', [])
        if commit:
            instance.save()
        return instance


class Step2EducationForm(forms.ModelForm):
    """Step 2: Education Details Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['current_status', 'highest_qualification', 'stream_specialization',
                  'college_name', 'university', 'graduation_year', 'academic_scores',
                  'has_backlogs', 'num_backlogs']
        widgets = {
            'current_status': forms.RadioSelect(),
            'highest_qualification': forms.Select(attrs={
                'class': 'form-control'
            }),
            'stream_specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science, Commerce, Arts'
            }),
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college name'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your university name'
            }),
            'graduation_year': forms.Select(attrs={
                'class': 'form-control'
            }),
            'academic_scores': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 8.5 CGPA or 75%'
            }),
            'has_backlogs': forms.RadioSelect(choices=[
                (True, 'Yes'),
                (False, 'No')
            ]),
            'num_backlogs': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def clean_has_backlogs(self):
        """Convert string 'true'/'false' from radio buttons to boolean"""
        value = self.data.get('has_backlogs')
        if value == 'true':
            return True
        elif value == 'false':
            return False
        return self.cleaned_data.get('has_backlogs', False)
    
    def clean_num_backlogs(self):
        has_backlogs = self.data.get('has_backlogs') == 'true'
        num_backlogs = self.cleaned_data.get('num_backlogs', 0)
        
        if has_backlogs and num_backlogs <= 0:
            raise ValidationError('Please specify the number of backlogs')
        
        return num_backlogs


class Step3SkillsForm(forms.ModelForm):
    """Step 3: Skills & Exposure Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['english_speaking', 'english_reading', 'english_writing',
                   'typing_speed']
        widgets = {
            'english_speaking': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'english_reading': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'english_writing': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'typing_speed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your typing speed in WPM',
                'min': '0',
                'max': '200'
            }),
        }
    
    # Computer skills checkboxes (matching template exactly)
    skill_ms_office = forms.BooleanField(required=False, label='MS Office')
    skill_google_sheets = forms.BooleanField(required=False, label='Google Suite')
    skill_email = forms.BooleanField(required=False, label='Email Communication')
    skill_internet = forms.BooleanField(required=False, label='Internet Browsing & Research')
    skill_social_media = forms.BooleanField(required=False, label='Social Media')
    
    # Tool exposure checkboxes (matching template exactly)
    tool_excel = forms.BooleanField(required=False, label='MS Excel / Google Sheets')
    tool_crm = forms.BooleanField(required=False, label='CRM Software')
    tool_design = forms.BooleanField(required=False, label='Design Tools')
    tool_video = forms.BooleanField(required=False, label='Video Conferencing')
    tool_programming = forms.BooleanField(required=False, label='Programming / Coding')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-populate computer skills
        if self.instance and self.instance.pk and self.instance.computer_skills:
            skill_map = {
                'MS Office': 'skill_ms_office',
                'Google Suite': 'skill_google_sheets',
                'Email Communication': 'skill_email',
                'Internet Browsing & Research': 'skill_internet',
                'Social Media': 'skill_social_media'
            }
            for skill in self.instance.computer_skills:
                field_name = skill_map.get(skill)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
        
        # Pre-populate tool exposure
        if self.instance and self.instance.pk and self.instance.tool_exposure:
            tool_map = {
                'MS Excel / Google Sheets': 'tool_excel',
                'CRM Software': 'tool_crm',
                'Design Tools': 'tool_design',
                'Video Conferencing': 'tool_video',
                'Programming / Coding': 'tool_programming'
            }
            for tool in self.instance.tool_exposure:
                field_name = tool_map.get(tool)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect computer skills
        skills = []
        skill_map = {
            'skill_ms_office': 'MS Office',
            'skill_google_sheets': 'Google Suite',
            'skill_email': 'Email Communication',
            'skill_internet': 'Internet Browsing & Research',
            'skill_social_media': 'Social Media'
        }
        for field, label in skill_map.items():
            if cleaned_data.get(field):
                skills.append(label)
        
        if not skills:
            raise ValidationError('Please select at least one computer skill')
        
        # Collect tool exposure
        tools = []
        tool_map = {
            'tool_excel': 'MS Excel / Google Sheets',
            'tool_crm': 'CRM Software',
            'tool_design': 'Design Tools',
            'tool_video': 'Video Conferencing',
            'tool_programming': 'Programming / Coding'
        }
        for field, label in tool_map.items():
            if cleaned_data.get(field):
                tools.append(label)
        
        cleaned_data['computer_skills'] = skills
        cleaned_data['tool_exposure'] = tools
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.computer_skills = self.cleaned_data.get('computer_skills', [])
        instance.tool_exposure = self.cleaned_data.get('tool_exposure', [])
        if commit:
            instance.save()
        return instance

class Step4CareerForm(forms.ModelForm):
    """Step 4: Career Preferences Form"""
    
    # Custom field for locations (will be converted from comma-separated string to list)
    preferred_locations = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Bangalore, Mumbai, Delhi'
        }),
        help_text='Enter cities separated by commas'
    )
    
    class Meta:
        model = StudentProfile
        fields = ['work_type', 'expected_salary', 'willing_to_relocate',
                  'preferred_job_roles', 'preferred_industries', 'preferred_locations']
        widgets = {
            'work_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'expected_salary': forms.Select(attrs={
                'class': 'form-control'
            }),
            'willing_to_relocate': forms.RadioSelect(choices=[
                (True, 'Yes'),
                (False, 'No')
            ]),
        }
    
    # Job roles checkboxes (matching template exactly)
    role_sales = forms.BooleanField(required=False, label='Sales / Business Development')
    role_customer_support = forms.BooleanField(required=False, label='Customer Support')
    role_marketing = forms.BooleanField(required=False, label='Marketing / Digital Marketing')
    role_hr = forms.BooleanField(required=False, label='Human Resources')
    role_content = forms.BooleanField(required=False, label='Content Writing')
    role_software_developer = forms.BooleanField(required=False, label='Software Developer')
    role_data_analyst = forms.BooleanField(required=False, label='Data Analyst')
    role_operations = forms.BooleanField(required=False, label='Operations / Admin')
    
    # Industries checkboxes (matching template exactly)
    industry_it_software = forms.BooleanField(required=False, label='IT / Software')
    industry_ecommerce = forms.BooleanField(required=False, label='E-commerce')
    industry_fintech = forms.BooleanField(required=False, label='Fintech / Banking')
    industry_edtech = forms.BooleanField(required=False, label='EdTech / Education')
    industry_healthcare = forms.BooleanField(required=False, label='Healthcare')
    industry_consulting = forms.BooleanField(required=False, label='Consulting')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-populate job roles
        if self.instance and self.instance.pk and self.instance.preferred_job_roles:
            role_map = {
                'Sales': 'role_sales',
                'Sales / Business Development': 'role_sales',
                'Customer Support': 'role_customer_support',
                'Marketing': 'role_marketing',
                'Marketing / Digital Marketing': 'role_marketing',
                'HR': 'role_hr',
                'Human Resources': 'role_hr',
                'Content': 'role_content',
                'Content Writing': 'role_content',
                'Software Developer': 'role_software_developer',
                'Data Analyst': 'role_data_analyst',
                'Operations': 'role_operations',
                'Operations / Admin': 'role_operations'
            }
            for role in self.instance.preferred_job_roles:
                field_name = role_map.get(role)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
        
        # Pre-populate industries
        if self.instance and self.instance.pk and self.instance.preferred_industries:
            industry_map = {
                'IT/Software': 'industry_it_software',
                'IT / Software': 'industry_it_software',
                'E-commerce': 'industry_ecommerce',
                'Fintech': 'industry_fintech',
                'Fintech / Banking': 'industry_fintech',
                'EdTech': 'industry_edtech',
                'EdTech / Education': 'industry_edtech',
                'Healthcare': 'industry_healthcare',
                'Consulting': 'industry_consulting'
            }
            for industry in self.instance.preferred_industries:
                field_name = industry_map.get(industry)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
        
        # Pre-populate locations (convert list to comma-separated string)
        if self.instance and self.instance.pk and self.instance.preferred_locations:
            self.initial['preferred_locations'] = ', '.join(self.instance.preferred_locations)
    
    def clean_willing_to_relocate(self):
        """Convert string 'true'/'false' from radio buttons to boolean"""
        value = self.data.get('willing_to_relocate')
        if value == 'true':
            return True
        elif value == 'false':
            return False
        return self.cleaned_data.get('willing_to_relocate', False)
    
    def clean_preferred_locations(self):
        """Convert comma-separated string to list"""
        locations_str = self.cleaned_data.get('preferred_locations', '')
        if locations_str:
            # Split by comma and clean up whitespace
            locations = [loc.strip() for loc in locations_str.split(',') if loc.strip()]
            return locations
        return []
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect job roles
        roles = []
        role_map = {
            'role_sales': 'Sales / Business Development',
            'role_customer_support': 'Customer Support',
            'role_marketing': 'Marketing / Digital Marketing',
            'role_hr': 'Human Resources',
            'role_content': 'Content Writing',
            'role_software_developer': 'Software Developer',
            'role_data_analyst': 'Data Analyst',
            'role_operations': 'Operations / Admin'
        }
        for field, label in role_map.items():
            if cleaned_data.get(field):
                roles.append(label)
        
        if not roles:
            raise ValidationError('Please select at least one preferred job role')
        
        # Collect industries
        industries = []
        industry_map = {
            'industry_it_software': 'IT / Software',
            'industry_ecommerce': 'E-commerce',
            'industry_fintech': 'Fintech / Banking',
            'industry_edtech': 'EdTech / Education',
            'industry_healthcare': 'Healthcare',
            'industry_consulting': 'Consulting'
        }
        for field, label in industry_map.items():
            if cleaned_data.get(field):
                industries.append(label)
        
        cleaned_data['preferred_job_roles'] = roles
        cleaned_data['preferred_industries'] = industries
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.preferred_job_roles = self.cleaned_data.get('preferred_job_roles', [])
        instance.preferred_industries = self.cleaned_data.get('preferred_industries', [])
        instance.preferred_locations = self.cleaned_data.get('preferred_locations', [])
        if commit:
            instance.save()
        return instance
    
class Step5AvailabilityForm(forms.ModelForm):
    """Step 5: Availability & Constraints Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['time_for_training', 'preferred_time_slots', 'has_mobile_access',
                  'has_laptop_access', 'internet_quality', 'constraints']
        widgets = {
            'time_for_training': forms.Select(attrs={
                'class': 'form-control'
            }),
            'has_mobile_access': forms.CheckboxInput(),
            'has_laptop_access': forms.CheckboxInput(),
            'internet_quality': forms.Select(attrs={
                'class': 'form-control'
            }),
            'constraints': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share any time constraints, health issues, or special requirements'
            }),
        }
    
    # Time slots checkboxes
    slot_morning = forms.BooleanField(required=False, label='Morning (6 AM - 12 PM)')
    slot_afternoon = forms.BooleanField(required=False, label='Afternoon (12 PM - 5 PM)')
    slot_evening = forms.BooleanField(required=False, label='Evening (5 PM - 9 PM)')
    slot_night = forms.BooleanField(required=False, label='Night (9 PM - 12 AM)')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-populate time slots
        if self.instance and self.instance.pk and self.instance.preferred_time_slots:
            slot_map = {
                'Morning': 'slot_morning',
                'Morning (6 AM - 12 PM)': 'slot_morning',
                'Afternoon': 'slot_afternoon',
                'Afternoon (12 PM - 5 PM)': 'slot_afternoon',
                'Evening': 'slot_evening',
                'Evening (5 PM - 9 PM)': 'slot_evening',
                'Night': 'slot_night',
                'Night (9 PM - 12 AM)': 'slot_night'
            }
            for slot in self.instance.preferred_time_slots:
                field_name = slot_map.get(slot)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect time slots
        slots = []
        slot_map = {
            'slot_morning': 'Morning (6 AM - 12 PM)',
            'slot_afternoon': 'Afternoon (12 PM - 5 PM)',
            'slot_evening': 'Evening (5 PM - 9 PM)',
            'slot_night': 'Night (9 PM - 12 AM)'
        }
        for field, label in slot_map.items():
            if cleaned_data.get(field):
                slots.append(label)
        
        if not slots:
            raise ValidationError('Please select at least one preferred time slot')
        
        cleaned_data['preferred_time_slots'] = slots
        
        # Validate at least one device is selected
        has_mobile = cleaned_data.get('has_mobile_access', False)
        has_laptop = cleaned_data.get('has_laptop_access', False)
        
        if not has_mobile and not has_laptop:
            raise ValidationError('Please select at least one device you have access to')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.preferred_time_slots = self.cleaned_data.get('preferred_time_slots', [])
        if commit:
            instance.save()
        return instance

class Step6BehaviouralForm(forms.ModelForm):
    """Step 6: Behavioural Fit Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['comfort_talking_strangers', 'comfort_handling_angry_customers',
                  'comfort_working_with_data', 'comfort_following_targets',
                  'comfort_writing_emails', 'people_vs_task_oriented',
                  'office_vs_remote', 'analysis_vs_communication',
                  'career_concerns', 'career_goal_3_years']
        widgets = {
            'comfort_talking_strangers': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comfort_handling_angry_customers': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comfort_working_with_data': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comfort_following_targets': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comfort_writing_emails': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'people_vs_task_oriented': forms.RadioSelect(),
            'office_vs_remote': forms.RadioSelect(),
            'analysis_vs_communication': forms.RadioSelect(),
            'career_goal_3_years': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Where do you see yourself in 3 years?'
            }),
        }
    
    # Career concerns checkboxes
    concern_lack_of_experience = forms.BooleanField(required=False, label='Lack of Experience')
    concern_lack_of_skills = forms.BooleanField(required=False, label='Lack of Skills')
    concern_low_confidence = forms.BooleanField(required=False, label='Low Confidence')
    concern_career_direction = forms.BooleanField(required=False, label='Career Direction')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-populate career concerns
        if self.instance and self.instance.pk and self.instance.career_concerns:
            concern_map = {
                'Lack of Experience': 'concern_lack_of_experience',
                'Lack of work experience': 'concern_lack_of_experience',
                'Lack of Skills': 'concern_lack_of_skills',
                'Need to develop more skills': 'concern_lack_of_skills',
                'Low Confidence': 'concern_low_confidence',
                'Low confidence': 'concern_low_confidence',
                'Career Direction': 'concern_career_direction',
                'Unclear about career direction': 'concern_career_direction'
            }
            for concern in self.instance.career_concerns:
                field_name = concern_map.get(concern)
                if field_name and field_name in self.fields:
                    self.initial[field_name] = True
    
    def clean_career_goal_3_years(self):
        goal = self.cleaned_data.get('career_goal_3_years', '').strip()
        if not goal:
            raise ValidationError('Please describe your career goal')
        if len(goal) < 20:
            raise ValidationError('Please provide more detail (minimum 20 characters)')
        return goal
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect career concerns
        concerns = []
        concern_map = {
            'concern_lack_of_experience': 'Lack of Experience',
            'concern_lack_of_skills': 'Lack of Skills',
            'concern_low_confidence': 'Low Confidence',
            'concern_career_direction': 'Career Direction'
        }
        for field, label in concern_map.items():
            if cleaned_data.get(field):
                concerns.append(label)
        
        cleaned_data['career_concerns'] = concerns
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.career_concerns = self.cleaned_data.get('career_concerns', [])
        if commit:
            instance.save()
        return instance

class Step7TrainingForm(forms.ModelForm):
    """Step 7: Training Program Information Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['previous_training', 'discovery_source', 'commitment_confirmed',
                  'fee_preference']
        widgets = {
            'previous_training': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe any previous training programs (or write "None")'
            }),
            'discovery_source': forms.Select(attrs={
                'class': 'form-control'
            }),
            'commitment_confirmed': forms.CheckboxInput(),
            'fee_preference': forms.RadioSelect(),
        }
    
    def clean_commitment_confirmed(self):
        commitment = self.cleaned_data.get('commitment_confirmed')
        if not commitment:
            raise ValidationError('Please confirm your commitment to the program')
        return commitment
    
    def clean_commitment_confirmed(self):
        commitment = self.cleaned_data.get('commitment_confirmed')
        if not commitment:
            raise ValidationError('Please confirm your commitment to the program')
        return commitment

class Step8DocumentsForm(forms.ModelForm):
    """Step 8: Document Uploads Form"""
    
    class Meta:
        model = StudentProfile
        fields = ['photo', 'resume', 'id_proof', 'marksheet']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'id_proof': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'marksheet': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError('Photo size should not exceed 5MB')
            # Check file type
            if not photo.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed for photo')
        return photo
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (max 10MB)
            if resume.size > 10 * 1024 * 1024:
                raise ValidationError('Resume size should not exceed 10MB')
        return resume