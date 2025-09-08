from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class OnlySelfMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения этого пользователя')
        return super().handle_no_permission()


class UserUpdateView(LoginRequiredMixin, OnlySelfMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменён')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Пользователь успешно удалён')
        return super().delete(request, *args, **kwargs)

