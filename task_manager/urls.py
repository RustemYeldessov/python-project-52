from django.contrib import admin
from django.urls import path, include
from .views import IndexView
from django.contrib.auth import views as auth_views
from task_manager.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),

    path('users/', include('task_manager.users.urls')),

    path('login/', user_views.UserLoginView.as_view(), name="login"),
    path('logout/', user_views.UserLogoutView.as_view(), name="logout"),

    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),  # 👈 добавь это
]