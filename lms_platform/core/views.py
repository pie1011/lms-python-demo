from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import UserProfile, Enrollment, Course, Assignment, Submission

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

# Student Portal Views
def student_login(request):
    """Student login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has student role
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'student':
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Access denied. Student accounts only.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Student profile not found.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'student/login.html')

@login_required
def student_dashboard(request):
    """Student dashboard showing enrolled courses"""
    # Check if user is a student
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'student':
            return HttpResponseForbidden("Access denied. Students only.")
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden("Student profile not found.")
    
    # Get student's enrollments and related data
    enrollments = Enrollment.objects.filter(
        student=request.user, 
        status='active'
    ).select_related('course', 'course__instructor')
    
    # Get recent assignments for enrolled courses
    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    recent_assignments = Assignment.objects.filter(
        module__course_id__in=enrolled_course_ids
    ).order_by('-created_at')[:5]
    
    # Get recent submissions by this student
    recent_submissions = Submission.objects.filter(
        student=request.user
    ).order_by('-submission_date')[:5]
    
    context = {
        'profile': profile,
        'enrollments': enrollments,
        'recent_assignments': recent_assignments,
        'recent_submissions': recent_submissions,
        'total_courses': enrollments.count(),
        'total_submissions': Submission.objects.filter(student=request.user).count(),
        'graded_submissions': Submission.objects.filter(student=request.user, status='graded').count(),
    }
    
    return render(request, 'student/dashboard.html', context)

def student_logout(request):
    """Student logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student_login')