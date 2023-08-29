from django.urls import path
from projects import views

urlpatterns = [
    path('add/', views.add_proj, name = 'add_or_change_proj'),
    path('view/', views.view_proj, name = 'view_proj'),
    path('analytics/', views.analytics_proj, name = 'analytics_proj'),
    path('info_project/<int:id>', views.info_proj, name = 'info_proj'),
    path('change_project/<int:id>', views.change_proj, name = 'change_proj'),
    path('delete_project/<int:id>', views.delete_proj, name = 'delete_proj')
]
