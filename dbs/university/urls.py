from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    # Student management URLs
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
] 