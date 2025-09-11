from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UsersListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"

class UserCreateView(CreateView):
    model = User
    template_name = "users/create.html"
    fields = ("username", "first_name", "last_name", "password")
    success_url = reverse_lazy("login")

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

