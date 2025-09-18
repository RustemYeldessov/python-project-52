from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'id_status'}),
            'executor': forms.Select(attrs={'class': 'form-control', 'id': 'id_executor'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_labels'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если в базе нет объектов, селекты будут пустыми — убедись, что есть данные для теста
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
        self.fields['labels'].queryset = Label.objects.all()