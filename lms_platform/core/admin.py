from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, Course, Module, Assignment, Enrollment, Submission
from django import forms

# Import the UserAdmin from Django's auth module to customize the User model admin
from django.contrib.auth.admin import UserAdmin

# For demo user admin restrictions
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class LMSAdminSite(admin.AdminSite):
    """
    Custom admin site that provides real data counts for the dashboard
    """
    site_title = "LMS Platform Admin"
    site_header = "LMS Platform Administration"
    index_title = "Welcome to LMS Platform Admin"
    
    def index(self, request, extra_context=None):
        """
        Override the default admin index to provide real data counts
        """
        extra_context = extra_context or {}
        
        # Get real counts from the database
        extra_context.update({
            # User counts
            'total_users': User.objects.count(),
            'total_profiles': UserProfile.objects.count(),
            'students_count': UserProfile.objects.filter(role='student').count(),
            'instructors_count': UserProfile.objects.filter(role='instructor').count(),
            'admins_count': UserProfile.objects.filter(role='admin').count(),
            
            # Academic content counts
            'total_courses': Course.objects.count(),
            'total_modules': Module.objects.count(),
            'total_assignments': Assignment.objects.count(),
            
            # Activity counts
            'total_enrollments': Enrollment.objects.count(),
            'active_enrollments': Enrollment.objects.filter(status='active').count(),
            'total_submissions': Submission.objects.count(),
            'graded_submissions': Submission.objects.filter(status='graded').count(),
            'pending_submissions': Submission.objects.filter(status='submitted').count(),
            
            # Recent activity (last 7 days)
            'recent_enrollments': Enrollment.objects.filter(
                enrollment_date__gte=timezone.now() - timedelta(days=7)
            ).count(),
        })
        
        return super().index(request, extra_context)


# Create our custom admin site instance
admin_site = LMSAdminSite(name='lms_admin')


class CourseAdmin(admin.ModelAdmin):
    """ Custom admin for Course model to filter instructors """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor":
            # Only show users who have instructor role
            instructor_profiles = UserProfile.objects.filter(role='instructor')
            instructor_users = [profile.user.id for profile in instructor_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=instructor_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EnrollmentAdmin(admin.ModelAdmin):
    """ Custom admin for Enrollment model to filter students """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            # Only show users who have student role
            student_profiles = UserProfile.objects.filter(role='student')
            student_users = [profile.user.id for profile in student_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=student_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SubmissionAdmin(admin.ModelAdmin):
    """ Custom admin for Submission model to filter students """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            # Only show users who have student role
            student_profiles = UserProfile.objects.filter(role='student')
            student_users = [profile.user.id for profile in student_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=student_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AssignmentAdminForm(forms.ModelForm):
    """ Custom form for Assignment model to handle specific field types and validation.
    This form allows for better control over how the fields are displayed in the admin interface.
    """
    class Meta:
        model = Assignment
        fields = '__all__'
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter assignment description...'
                }
            ),
            'instructions': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': 'Enter detailed instructions for students...'
                }
            ),
        }


class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentAdminForm
    list_display = ['assignment_name', 'module', 'due_date', 'max_points', 'assignment_type']
    list_filter = ['assignment_type', 'due_date', 'module__course']
    search_fields = ['assignment_name', 'description']


# Custom mixin to restrict demo user actions
class DemoUserMixin:
    """
    Mixin to allow demo users full visual access but prevent actual changes
    """
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def save_model(self, request, obj, form, change):
        """Prevent demo users from saving any data"""
        if request.user.username == 'PortfolioDemo':
            return  # Don't save anything for demo users
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Prevent demo users from deleting data"""
        if request.user.username == 'PortfolioDemo':
            return  # Don't delete anything for demo users
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Prevent demo users from bulk deleting data"""
        if request.user.username == 'PortfolioDemo':
            return  # Don't delete anything for demo users
        super().delete_queryset(request, queryset)
    
    def response_add(self, request, obj, post_url_continue=None):
        """Handle demo user add responses"""
        if request.user.username == 'PortfolioDemo':
            messages.success(
                request,
                f'Demo Mode: {self.model._meta.verbose_name} would have been created successfully! '
                f'The form validation and interface work perfectly, but no actual data was modified for this demonstration.'
            )
            return HttpResponseRedirect(
                reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
            )
        return super().response_add(request, obj, post_url_continue)
    
    def response_change(self, request, obj):
        """Handle demo user change responses"""
        if request.user.username == 'PortfolioDemo':
            messages.success(
                request,
                f'Demo Mode: {self.model._meta.verbose_name} would have been updated successfully! '
                f'The form validation and interface work perfectly, but no actual data was modified for this demonstration.'
            )
            return HttpResponseRedirect(
                reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
            )
        return super().response_change(request, obj)
    
    def delete_view(self, request, object_id, extra_context=None):
        """Override delete view for demo users"""
        if request.user.username == 'PortfolioDemo':
            messages.success(
                request,
                f'Demo Mode: {self.model._meta.verbose_name} would have been deleted successfully! '
                f'The delete process works perfectly, but no actual data was removed for this demonstration.'
            )
            return HttpResponseRedirect(
                reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
            )
        return super().delete_view(request, object_id, extra_context)
    
    def get_actions(self, request):
        """Override bulk actions for demo users"""
        actions = super().get_actions(request)
        if request.user.username == 'PortfolioDemo':
            # Remove the delete action for demo users but keep others for demonstration
            if 'delete_selected' in actions:
                actions['delete_selected'] = (
                    self._demo_delete_selected,
                    'delete_selected',
                    'Delete selected %(verbose_name_plural)s'
                )
        return actions
    
    def _demo_delete_selected(self, request, queryset):
        """Demo-safe bulk delete action"""
        messages.success(
            request,
            f'Demo Mode: {queryset.count()} {self.model._meta.verbose_name_plural} would have been deleted successfully! '
            f'The bulk delete process works perfectly, but no actual data was removed for this demonstration.'
        )
        return HttpResponseRedirect(
            reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')
        )


# Update existing admin classes to use the mixin
class CourseAdmin(DemoUserMixin, admin.ModelAdmin):
    """ Custom admin for Course model to filter instructors """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor":
            # Only show users who have instructor role
            instructor_profiles = UserProfile.objects.filter(role='instructor')
            instructor_users = [profile.user.id for profile in instructor_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=instructor_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EnrollmentAdmin(DemoUserMixin, admin.ModelAdmin):
    """ Custom admin for Enrollment model to filter students """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            # Only show users who have student role
            student_profiles = UserProfile.objects.filter(role='student')
            student_users = [profile.user.id for profile in student_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=student_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SubmissionAdmin(DemoUserMixin, admin.ModelAdmin):
    """ Custom admin for Submission model to filter students """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            # Only show users who have student role
            student_profiles = UserProfile.objects.filter(role='student')
            student_users = [profile.user.id for profile in student_profiles]
            kwargs["queryset"] = User.objects.filter(id__in=student_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AssignmentAdmin(DemoUserMixin, admin.ModelAdmin):
    form = AssignmentAdminForm
    list_display = ['assignment_name', 'module', 'due_date', 'max_points', 'assignment_type']
    list_filter = ['assignment_type', 'due_date', 'module__course']
    search_fields = ['assignment_name', 'description']


# Add mixin to other admin classes
class UserProfileAdmin(DemoUserMixin, admin.ModelAdmin):
    pass


class ModuleAdmin(DemoUserMixin, admin.ModelAdmin):
    pass



# Register models with both the default admin and our custom admin
# Default admin (keep existing functionality)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Submission, SubmissionAdmin)

# Custom admin with dashboard data AND demo user restrictions
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Module, ModuleAdmin)
admin_site.register(Assignment, AssignmentAdmin)
admin_site.register(Enrollment, EnrollmentAdmin)
admin_site.register(Submission, SubmissionAdmin)

# Register Django's built-in User model with demo restrictions
from django.contrib.auth.admin import UserAdmin
class DemoUserAdmin(DemoUserMixin, UserAdmin):
    """Custom User admin with hidden password details and demo protections"""
    
    # Explicitly set all necessary attributes
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def get_fieldsets(self, request, obj=None):
        """Override fieldsets to hide password details but keep functionality"""
        # Get Django's default fieldsets
        default_fieldsets = super().get_fieldsets(request, obj)
        
        # Filter out password field from the default fieldsets
        filtered_fieldsets = []
        for name, field_options in default_fieldsets:
            fields = field_options.get('fields', ())
            
            # Remove password field if present
            if 'password' in fields:
                new_fields = tuple(field for field in fields if field != 'password')
                if new_fields:  # Only add if there are remaining fields
                    filtered_fieldsets.append((name, {**field_options, 'fields': new_fields}))
            else:
                filtered_fieldsets.append((name, field_options))
        
        return tuple(filtered_fieldsets)
    
    def get_readonly_fields(self, request, obj=None):
        """Get readonly fields for user admin"""
        # Get the default readonly fields from parent class
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        if obj and obj.username == 'PortfolioDemo':
            # For demo users, make more fields readonly
            readonly_fields.extend(['username', 'is_staff', 'is_superuser'])
        
        return readonly_fields
    
    def user_change_password(self, request, id, form_url=''):
        """Override password change view to block demo users"""
        try:
            user = self.get_object(request, id)
            if user and user.username == 'PortfolioDemo':
                messages.error(
                    request, 
                    'Password changes are disabled for the demo account.'
                )
                return HttpResponseRedirect(
                    reverse('admin:auth_user_change', args=[id])
                )
        except:
            pass
        return super().user_change_password(request, id, form_url)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override change view to ensure password change functionality"""
        extra_context = extra_context or {}
        
        # Ensure the password change link appears for authorized users
        if object_id:
            try:
                user = self.get_object(request, object_id)
                if user:
                    # Django checks for this specific context variable
                    # Show password change for superusers, but not for demo users
                    extra_context['has_change_password_permission'] = (
                        user.username != 'PortfolioDemo' and
                        request.user.is_superuser and
                        self.has_change_permission(request, user)
                    )
                    # Also set show_password_fields to True for non-demo users
                    extra_context['show_password_fields'] = user.username != 'PortfolioDemo'
            except:
                extra_context['has_change_password_permission'] = False
                extra_context['show_password_fields'] = False
                
        return super().change_view(request, object_id, form_url, extra_context)

# Register with both admin sites to ensure password functionality works
admin.site.unregister(User)  # Unregister the default User admin first
admin.site.register(User, DemoUserAdmin)
admin_site.register(User, DemoUserAdmin)