from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from lms_platform.core.models import UserProfile


class Command(BaseCommand):
    help = 'Create a demo user for portfolio viewing (read-only access)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating demo user for portfolio...'))

        # Create or get the demo user
        username = 'PortfolioDemo'
        password = 'ViewOnly123'
        
        demo_user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'demo@katieharshman.com',
                'first_name': 'Portfolio',
                'last_name': 'Demo',
                'is_staff': True,  # Can access admin
                'is_superuser': False,  # Not a superuser
                'is_active': True
            }
        )
        
        if created:
            demo_user.set_password(password)
            demo_user.save()
            self.stdout.write(f'✅ Created demo user: {username}')
        else:
            # Update password in case it changed
            demo_user.set_password(password)
            demo_user.save()
            self.stdout.write(f'✅ Updated demo user: {username}')
        
        # Create or update user profile
        demo_profile, profile_created = UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={
                'role': 'admin',
                'first_name': 'Portfolio',
                'last_name': 'Demo',
                'phone_number': '555-DEMO'
            }
        )
        
        if profile_created:
            self.stdout.write('✅ Created demo user profile')
        else:
            self.stdout.write('✅ Demo user profile already exists')
        
        # Clear existing permissions
        demo_user.user_permissions.clear()
        
        # Add only VIEW permissions for all our models
        from lms_platform.core.models import Course, Module, Assignment, Enrollment, Submission
        
        models_to_allow = [
            User, UserProfile, Course, Module, Assignment, Enrollment, Submission
        ]
        
        for model in models_to_allow:
            content_type = ContentType.objects.get_for_model(model)
            
            # Add view permission (Django 2.1+ has built-in view permission)
            try:
                view_permission = Permission.objects.get(
                    codename=f'view_{model._meta.model_name}',
                    content_type=content_type
                )
                demo_user.user_permissions.add(view_permission)
                self.stdout.write(f'   ✅ Added view permission for {model._meta.model_name}')
            except Permission.DoesNotExist:
                self.stdout.write(f'   ⚠️  View permission not found for {model._meta.model_name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Demo user created successfully!\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Access: Read-only (can view but not modify)\n'
                f'Perfect for portfolio demonstrations!'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\n📝 Add these credentials to your portfolio:\n'
                f'   Username: {username}\n'
                f'   Password: {password}\n'
                '   Note: Read-only access for demonstration purposes'
            )
        )