from django.urls import path
from tasks import views

urlpatterns = [
    path('create_task', views.create_task, name = 'create_task'),
    path('change_admin_task/<int:id>', views.change_admin_task, name = 'change_admin_task'),
    path('view_created_task/', views.view_created_tasks, name = 'view_created_tasks'),
    path('view_available_tasks/', views.view_available_tasks, name = 'view_available_tasks'),
    path('view_appointed_tasks/', views.view_appointed_tasks, name = 'view_appointed_tasks'),
    path('info_task/<int:id>', views.info_task, name = 'info_task'),
    path('change_task/<int:id>', views.change_task, name = 'change_task'),
    path('delete_task/<int:id>', views.delete_task, name = 'delete_task'),
    
]
