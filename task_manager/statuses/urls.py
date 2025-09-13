from django.urls import path
from . import views

urlpatterns = [
    path('', views.StatusListView.as_view(), name='statuses_index'),
    path('create/', views.CreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='status_delete'),
]
