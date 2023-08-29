from django.urls import path
from users import views

urlpatterns = [
    path('view/', views.view_users, name = 'view_users'),
]
