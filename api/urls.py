from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipe_list, name = 'recipe-list'),
    path('recipes/<int:pk>/', views.recipe_detail, name = 'recipe-detail'),
    path('admin-only-view/', views.admin_only_view, name = 'admin-view-only'),
    path('api/logout/', views.logout_view, name='logout'),
]