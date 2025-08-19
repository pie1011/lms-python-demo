from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends Django's built-in User model with LMS-specific profile information.
    Stores role-based information and additional profile details for students,
    instructors, and administrators in the learning management system.
    """

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Course(models.Model):
    """
    Represents an academic course offered in a specific term.
    A course is taught by one instructor per term and can have multiple students
    enrolled. The same course (e.g., MATH101) can be offered in different terms
    with different instructors.
    """ 

    course_code = models.CharField(max_length=20, unique=True)  # e.g., "MATH101"
    course_name = models.CharField(max_length=200)  # e.g., "Introduction to Mathematics"
    description = models.TextField()
    credits = models.PositiveIntegerField()
    term = models.CharField(max_length=50)  # e.g., "Spring 2024"
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    max_enrollment = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name} ({self.term})"
    
    class Meta:
        unique_together = ['course_code', 'term']  # Same course can exist in different terms

class Module(models.Model):
    """
    Represents a learning module within a course.
    Modules organize course content into logical sections (e.g., "Module 1: Addition").
    Each module belongs to one course and contains multiple assignments.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    module_name = models.CharField(max_length=200)  # e.g., "Module 1: Addition"
    description = models.TextField()
    order_number = models.PositiveIntegerField()  # For sequencing modules
    content = models.TextField()  # Lesson material/content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.course_code} - {self.module_name}"
    
    class Meta:
        unique_together = ['course', 'order_number']  # No duplicate order numbers per course
        ordering = ['course', 'order_number']


class Assignment(models.Model):
    """
    Represents an assignment within a specific module.
    Assignments are tasks/assessments that students complete and submit for grading.
    Each assignment belongs to one module and can have multiple student submissions.
    """

    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('project', 'Project'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assignments')
    assignment_name = models.CharField(max_length=200)  # e.g., "Addition Homework"
    description = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.PositiveIntegerField()  # Total points possible
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    instructions = models.TextField()  # Detailed instructions for students
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.module.course.course_code} - {self.assignment_name}"
    
    class Meta:
        ordering = ['due_date']

class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific course.
    Tracks the many-to-many relationship between students and courses,
    along with enrollment status and grade information.
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    current_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 85.50
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Locked at term end
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    gpa_points = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # For GPA calculation
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_code}"
    
    class Meta:
        unique_together = ['student', 'course']  # Student can only enroll once per course

class Submission(models.Model):
    """
    Represents a student's submission for a specific assignment.
    Tracks student work, grading, and feedback. This is where individual
    assignment grades are stored and connected to the overall course grade.
    """
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_content = models.TextField(blank=True)  # Text response
    file_upload = models.FileField(upload_to='submissions/', blank=True, null=True)  # File uploads
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Points received
    feedback = models.TextField(blank=True)  # Instructor comments
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    graded_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.assignment_name}"
    
    class Meta:
        unique_together = ['student', 'assignment']  # One submission per student per assignment
        ordering = ['-submission_date']