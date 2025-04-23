from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course', views.course, name='course'),
    path('detail', views.course_details, name="course_detail"),
    path('course_upload', views.course_upload, name="course_upload"),

    path('dashboard', views.user_dashboard, name="user_dashboard"),
    path('profile', views.profile, name="profile"),
    path('timetable', views.timetable, name="timetable"),
    path('mycourses', views.mycourse, name="mycourse"),
    path('assignments', views.assignments, name="assignments"),

    path('account_settings', views.account_settings, name="account_settings"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('password_reset', views.password_reset, name='password_reset')
]