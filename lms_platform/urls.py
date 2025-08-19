"""
URL configuration for lms_platform project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from lms_platform.core import views as core_views
from lms_platform.core.admin import admin_site


urlpatterns = [
    path("", core_views.index, name='index'), 
    path("admin/", admin_site.urls),
    
    # Student Portal URLs
    path("student/", core_views.student_dashboard, name='student_dashboard'),
    path("student/login/", core_views.student_login, name='student_login'),
    path("student/logout/", core_views.student_logout, name='student_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)