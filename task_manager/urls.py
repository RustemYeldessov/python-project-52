"""
URL configuration for task_manager project.
"""
from django.contrib import admin
from django.urls import path
from .views import IndexView
from django.contrib.auth import views as auth_views
from task_manager.users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="home"),
    path('users/', user_views.UsersListView.as_view(), name="users_index"),
    path('users/create/', user_views.UserCreateView.as_view(), name="users_create"),
    path('users/<int:pk>/update/', user_views.UserUpdateView.as_view(), name="users_update"),
    path('users/<int:pk>/delete/', user_views.UserDeleteView.as_view(), name="users_delete"),

    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
