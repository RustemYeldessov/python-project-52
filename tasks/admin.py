from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для управления задачами."""
    
    list_display = [
        'title',
        'status',
        'created_by',
        'assigned_to',
        'created_at',
        'due_date'
    ]
    list_filter = [
        'status',
        'created_at',
        'due_date',
        'created_by',
        'assigned_to'
    ]
    search_fields = [
        'title',
        'description',
        'created_by__username',
        'assigned_to__username'
    ]
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'status')
        }),
        ('Назначение', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Временные рамки', {
            'fields': ('due_date',)
        }),
    )