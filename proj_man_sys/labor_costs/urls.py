from django.urls import path
from labor_costs import views

urlpatterns = [
    path('create/', views.create_labor_costs, name = 'create'),
    path('view/', views.view_labor_costs, name = 'view_labor_costs'),
    path('delete_labor/<int:id>', views.delete_labor, name = 'delete_labor')
]
