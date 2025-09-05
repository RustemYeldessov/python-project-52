"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.views.generic import TemplateView


def home(request):
    """Главная страница приложения."""
    return HttpResponse("""
    <html>
        <head>
            <title>Task Manager</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 600px; margin: 0 auto; }
                h1 { color: #333; }
                .status { background: #e8f5e8; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Task Manager</h1>
                <div class="status">
                    <h2>✅ Проект успешно настроен!</h2>
                    <p>Django приложение работает корректно.</p>
                    <p>Версия Django: 5.2.6</p>
                    <p>База данных: SQLite (по умолчанию)</p>
                </div>
            </div>
        </body>
    </html>
    """)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", home, name="home"),  # используем функцию home
    # или вариант через шаблон:
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
