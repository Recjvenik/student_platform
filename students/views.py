from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import StudentProfile, Experience
import json


@login_required
def profile_start(request):
    """Start or continue profile registration"""
    
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.name or '',
            'step_completed': 0
        }
    )
    
    # If profile is complete, redirect to dashboard
    if profile.is_complete:
        return redirect('dashboard')
    
    # Redirect to the next incomplete step
    next_step = profile.step_completed + 1
    if next_step > 8:
        next_step = 8
    
    return redirect('profile_step', step=next_step)


@login_required
def profile_step(request, step):
    """Display and handle individual profile steps"""
    
    step = int(step)
    if step < 1 or step > 8:
        return redirect('profile_start')
    
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    # Prevent skipping steps
    if step > profile.step_completed + 1:
        return redirect('profile_step', step=profile.step_completed + 1)
    
    context = {
        'step': step,
        'profile': profile,
        'total_steps': 8,
    }
    
    # Get template based on step
    template_map = {
        1: 'students/step1_basic.html',
        2: 'students/step2_education.html',
        3: 'students/step3_skills.html',
        4: 'students/step4_career.html',
        5: 'students/step5_availability.html',
        6: 'students/step6_behavioural.html',
        7: 'students/step7_training.html',
        8: 'students/step8_documents.html',
    }
    
    return render(request, template_map.get(step), context)


@login_required
@require_http_methods(["POST"])
def save_step(request):
    """AJAX endpoint to save step data"""
    
    try:
        data = json.loads(request.body)
        step = int(data.get('step', 0))
        
        profile = get_object_or_404(StudentProfile, user=request.user)
        
        # Save data based on step
        if step == 1:
            # Basic Information
            profile.full_name = data.get('full_name', '')
            profile.gender = data.get('gender', '')
            profile.date_of_birth = data.get('date_of_birth', '')
            profile.current_city = data.get('current_city', '')
            profile.current_state = data.get('current_state', '')
            profile.preferred_languages = data.get('preferred_languages', [])
            
        elif step == 2:
            # Education
            profile.current_status = data.get('current_status', '')
            profile.highest_qualification = data.get('highest_qualification', '')
            profile.stream_specialization = data.get('stream_specialization', '')
            profile.college_name = data.get('college_name', '')
            profile.university = data.get('university', '')
            profile.graduation_year = int(data.get('graduation_year', 2024))
            profile.academic_scores = data.get('academic_scores', '')
            profile.has_backlogs = data.get('has_backlogs', False)
            profile.num_backlogs = int(data.get('num_backlogs', 0))
            
            # Handle experiences
            experiences = data.get('experiences', [])
            # Clear existing experiences
            profile.experiences.all().delete()
            # Create new ones
            for exp in experiences:
                Experience.objects.create(
                    student_profile=profile,
                    company_name=exp.get('company_name', ''),
                    role=exp.get('role', ''),
                    duration=exp.get('duration', ''),
                    description=exp.get('description', '')
                )
            
        elif step == 3:
            # Skills
            profile.english_speaking = int(data.get('english_speaking', 3))
            profile.english_reading = int(data.get('english_reading', 3))
            profile.english_writing = int(data.get('english_writing', 3))
            profile.computer_skills = data.get('computer_skills', [])
            profile.tool_exposure = data.get('tool_exposure', [])
            profile.typing_speed = int(data.get('typing_speed', 0))
            
        elif step == 4:
            # Career Preferences
            profile.preferred_job_roles = data.get('preferred_job_roles', [])
            profile.preferred_industries = data.get('preferred_industries', [])
            profile.work_type = data.get('work_type', '')
            profile.preferred_locations = data.get('preferred_locations', [])
            profile.willing_to_relocate = data.get('willing_to_relocate', False)
            profile.expected_salary = data.get('expected_salary', '')
            
        elif step == 5:
            # Availability
            profile.time_for_training = data.get('time_for_training', '')
            profile.preferred_time_slots = data.get('preferred_time_slots', [])
            profile.has_mobile_access = data.get('has_mobile_access', True)
            profile.has_laptop_access = data.get('has_laptop_access', False)
            profile.internet_quality = data.get('internet_quality', '')
            profile.constraints = data.get('constraints', '')
            
        elif step == 6:
            # Behavioural
            profile.comfort_talking_strangers = int(data.get('comfort_talking_strangers', 3))
            profile.comfort_handling_angry_customers = int(data.get('comfort_handling_angry_customers', 3))
            profile.comfort_working_with_data = int(data.get('comfort_working_with_data', 3))
            profile.comfort_following_targets = int(data.get('comfort_following_targets', 3))
            profile.comfort_writing_emails = int(data.get('comfort_writing_emails', 3))
            profile.people_vs_task_oriented = data.get('people_vs_task_oriented', '')
            profile.office_vs_remote = data.get('office_vs_remote', '')
            profile.analysis_vs_communication = data.get('analysis_vs_communication', '')
            profile.career_concerns = data.get('career_concerns', [])
            profile.career_goal_3_years = data.get('career_goal_3_years', '')
            
        elif step == 7:
            # Training Info
            profile.previous_training = data.get('previous_training', '')
            profile.discovery_source = data.get('discovery_source', '')
            profile.commitment_confirmed = data.get('commitment_confirmed', False)
            profile.fee_preference = data.get('fee_preference', '')
        
        # Update step completed
        if step > profile.step_completed:
            profile.step_completed = step
        
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Step saved successfully',
            'step_completed': profile.step_completed
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def profile_review(request):
    """Review all entered data before final submission"""
    
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    if profile.step_completed < 7:
        return redirect('profile_step', step=profile.step_completed + 1)
    
    experiences = profile.experiences.all()
    
    context = {
        'profile': profile,
        'experiences': experiences,
    }
    
    return render(request, 'students/review.html', context)


@login_required
@require_http_methods(["POST"])
def profile_submit(request):
    """Final submission of profile"""
    
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    # Mark as complete
    profile.is_complete = True
    profile.step_completed = 8
    profile.submitted_at = timezone.now()
    profile.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Profile submitted successfully!',
        'redirect': '/dashboard/'
    })


@login_required
def dashboard(request):
    """User dashboard after profile completion"""
    
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('profile_start')
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'students/dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def upload_documents(request):
    """Handle document uploads"""
    
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    if 'photo' in request.FILES:
        profile.photo = request.FILES['photo']
    if 'resume' in request.FILES:
        profile.resume = request.FILES['resume']
    if 'id_proof' in request.FILES:
        profile.id_proof = request.FILES['id_proof']
    if 'marksheet' in request.FILES:
        profile.marksheet = request.FILES['marksheet']
    
    profile.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Documents uploaded successfully'
    })