from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status created successfully')

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status changed successfully')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _("Status deleted successfully")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(
                self.request,
                _("It is impossible to delete the status \
                    because it is being used")
            )
            return redirect(self.success_url)


