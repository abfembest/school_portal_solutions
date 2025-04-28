from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Course, Country

# Create your views here.
def home(request):
    return render(request, 'home.html')

def course(request):
    return render(request, 'courses.html')

def course_details(request):
    return render(request, 'courses-details.html')

def course_upload(request):
    return render(request, 'course-upload.html')

def events(request):
    return render(request, 'events.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        course_name = request.POST.get('course')
        country_name = request.POST.get('country')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate form data
        if not all([first_name, last_name, email, course_name, country_name, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        try:
            # Get or create course and country
            course_obj, _ = Course.objects.get_or_create(
                name=course_name,
                defaults={'description': f'Course for {course_name}', 'price': 0.00}
            )
            country_obj, _ = Country.objects.get_or_create(name=country_name)

            # Create user
            username = email  # Using email as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create profile
            Profile.objects.create(
                user=user,
                course=course_obj,
                country=country_obj
            )

            messages.success(request, "Registration successful. Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')
    
    return render(request, 'signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Try to find the user by email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('user_dashboard')  # Redirect to dashboard or home page
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    
    return render(request, 'signin.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('login')

def password_reset(request):
    return 'Hi'

#Student Views
def user_dashboard(request):
    return render(request, 'student/user_dashboard.html')

def profile(request):
    return render(request, 'student/profile.html')

def account_settings(request):
    return render(request, 'student/settings.html')

def timetable(request):
    return render(request, 'student/timetable.html')

def mycourse(request):
    return render(request, 'student/courses.html')

def assignments(request):
    return render(request, 'student/assignments.html')

def grade_reports(request):
    return render(request, 'student/grades&report.html')

def attendance(request):
    return render(request, 'student/attendance.html')

#Teacher Views
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')

def t_profile(request):
    return render(request, 'teacher/profile.html')

def myclasses(request):
    return render(request, 'teacher/classes.html')

def ttimetable(request):
    return render(request, 'teacher/timetable.html')

def m_assignment(request):
    return render(request, 'teacher/manage_assignment.html')

def grade_book(request):
    return render(request, 'teacher/grade_book.html')

def attendance_manager(request):
    return render(request, 'teacher/attendance_manager.html')

def messaging(request):
    return render(request, 'teacher/messaging.html')

def course_resource(request):
    return render(request, 'teacher/course_resource.html')

#Parent Views
def parent_dashboard(request):
    return render(request, 'parent/dashboard.html')

def p_profile(request):
    return render(request, 'parent/profile.html')

def child_profile(request):
    return render(request, 'parent/child_profile.html')

def classwork(request):
    return render(request, 'parent/classwork.html')

def school_calendar(request):
    return render(request, 'parent/calendar.html')

def grades_report(request):
    return render(request, 'parent/grade_reports.html')

def child_attendance(request):
    return render(request, 'parent/attendance.html')

def chats(request):
    return render(request, 'parent/messages.html')

def payment(request):
    return render(request, 'parent/payment.html')

def announcements(request):
    return render(request, 'parent/announcements.html')