from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('course', views.course, name='course'),
    path('detail/<int:id>', views.course_details, name="course_detail"),
    path('course_upload', views.course_upload, name="course_upload"),

    path('s/home', views.user_dashboard, name="user_dashboard"),
    path('s/profile', views.profile, name="profile"),
    path('s/timetable', views.timetable, name="timetable"),
    path('s/mycourses', views.mycourse, name="mycourse"),
    path('s/assignments', views.assignments, name="assignments"),
    path('s/grade', views.grade_reports, name="grades"),
    path('s/attendance', views.attendance, name="attendance"),

    # Teacher Urls
    path('t/home', views.teacher_dashboard, name="teacher_dashboard"),
    path('t/profile', views.t_profile, name="t_profile"),
    path('t/classes', views.myclasses, name="my_classes"),
    path('t/timetable', views.ttimetable, name="t_timetable"),
    path('t/assignment', views.m_assignment, name="m_assignments"),
    path('t/gradebook', views.grade_book, name="grade_book"),
    path('t/attendance', views.attendance_manager, name="attendance_manager"),
    path('t/message', views.messaging, name="messaging"),
    path('t/course_resources', views.course_resource, name="course_resource"),

    # Parent Urls
    path('p/home', views.parent_dashboard, name="parent_dashboard"),
    path('p/profile', views.p_profile, name="p_profile"),
    path('p/child_profile', views.child_profile, name="child_profile"),
    path('p/classwork', views.classwork, name="classwork"),
    path('p/calendar', views.school_calendar, name="school_calendar"),
    path('p/grades_reports', views.grades_report, name="grades_report"),
    path('p/attendance', views.child_attendance, name="child_attendance"),
    path('p/message', views.chats, name="chat"),
    path('p/payment', views.payment, name="payment"),
    path('p/notice', views.announcements, name="announcements"),

    # Admin Urls
    path('a/home', views.admin_dashboard, name="admin_dashboard"),
    path('a/users', views.manage_users, name="manage_users"),
    path('a/course', views.courses, name="courses_classes"),
    path('a/curriculum', views.curriculum, name="curriculum"),
    path('a/calendar', views.calendar, name="calendar"),
    path('a/analytics', views.analytics, name="analytics"),
    path('a/attendance', views.attendance, name="attendance"),
    path('a/communications', views.communications, name="communications"),
    path('a/finance_fees', views.finance_fees, name="finance_fees"),
    path('a/document_management', views.document_management, name="document_management"),

    path('account_settings', views.account_settings, name="account_settings"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('events', views.events, name='events')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)