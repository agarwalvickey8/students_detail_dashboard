# staffsignup/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('student-list/', views.student_list_view, name='student_list'),
    path('edit-neet-registration/<int:neet_registration_id>/', views.edit_neet_registration, name='edit_neet_registration'),
    path('logout/', views.logout, name='logout'),
]
