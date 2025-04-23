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

#User Code
def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

def profile(request):
    return render(request, 'user/profile.html')

def account_settings(request):
    return render(request, 'settings.html')

def timetable(request):
    return render(request, 'user/timetable.html')

def mycourse(request):
    return render(request, 'user/courses.html')


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
