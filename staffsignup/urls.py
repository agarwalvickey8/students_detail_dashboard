# staffsignup/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('student-list/', views.student_list_view, name='student_list'),
    path('edit-registration/<int:registration_id>/', views.edit_registration, name='edit_registration'),
    path('logout/', views.logout, name='logout'),
    path('update_field/', views.update_field, name='update_field'),
]
