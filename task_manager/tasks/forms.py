from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_executor'}
        ),
        label=Task._meta.get_field('executor').verbose_name,
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={
                'class':
                    'form-control'}
            ),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_status'}
            ),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'id_labels'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
        self.fields['executor'].label_from_instance = (
            lambda u: f"{u.first_name} {u.last_name}".strip()
        )