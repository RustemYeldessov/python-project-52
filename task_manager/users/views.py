from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserLoginForm
from .forms import UserCreateForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UsersListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = gettext_lazy("Пользователь успешно зарегистрирован")

class UserUpdateView(UpdateView):
    model = User
    template_name = "users/update.html"
    fields = ("username", "first_name", "last_name", "password")
    success_url = reverse_lazy("users_index")

    def test_func(self):
        return self.request.user == self.get_object()

class UserDeleteView(DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_index")

    def test_func(self):
        return self.request.user == self.get_object()


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = gettext_lazy("You are logged in")

    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, gettext_lazy("You are logged out"))
        return super().dispatch(request, *args, **kwargs)