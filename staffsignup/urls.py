from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('student-list/', views.student_list_view, name='student_list'),
    path('logout/', views.logout, name='logout'),
    path('update_field/', views.update_field, name='update_field'),
    path('get_batch_options/', views.get_batch_options, name='get_batch_options'),
    path('review-page/', views.review_page, name='review_page')
]
