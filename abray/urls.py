from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course', views.course, name='course'),
    path('detail', views.course_details, name="course_detail"),
    path('course_upload', views.course_upload, name="course_upload"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('password_reset', views.password_reset, name='password_reset')
]