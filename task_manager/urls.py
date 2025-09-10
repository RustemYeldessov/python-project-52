"""
URL configuration for task_manager project.
"""
from django.contrib import admin
from django.urls import path
from .views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="home"),
]
