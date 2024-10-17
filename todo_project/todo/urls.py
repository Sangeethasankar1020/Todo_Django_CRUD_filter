# todo/urls.py

from django.urls import path
from .views import home, add_task, update_task, delete_task

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_task, name='add_task'),
    path('update/<str:task_id>/', update_task, name='update_task'),
    path('delete/<str:task_id>/', delete_task, name='delete_task'),
]
