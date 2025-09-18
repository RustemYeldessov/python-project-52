from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status  # <- именно эта модель


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }