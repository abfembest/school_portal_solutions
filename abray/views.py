from django.contrib import messages
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Profile, Course, Country, CourseModule, Lesson, Instructor, Review, Category

# Create your views here.
def home(request):
    return render(request, 'home.html')

def course(request):
    """View to display all active courses"""
    courses = Course.objects.all()
    
    # # Filter by category if provided
    # category_slug = request.GET.get('category')
    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     courses = courses.filter(category=category)
    
    # # Filter by difficulty level if provided
    # difficulty = request.GET.get('difficulty')
    # if difficulty:
    #     courses = courses.filter(difficulty_level=difficulty)
        
    # Get all categories for the filter sidebar
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses.html', context)

def course_detail(request, slug):
    """View to display a single course with all its details"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    # Get course modules and their lessons
    modules = CourseModule.objects.filter(course=course).prefetch_related('lessons')
    
    # Get course instructor
    instructor = Instructor.objects.get(user = course.instructor)
    # instructor = get_object_or_404(Instructor, user=course.instructor)
    print('This is it', instructor)
    
    # Get course reviews
    reviews = Review.objects.filter(course=course)
    review_count = reviews.count()
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Calculate rating distribution
    rating_distribution = {
        5: reviews.filter(rating=5).count(),
        4: reviews.filter(rating=4).count(),
        3: reviews.filter(rating=3).count(), 
        2: reviews.filter(rating=2).count(),
        1: reviews.filter(rating=1).count()
    }
    
    # Convert to percentages if there are reviews
    if review_count > 0:
        for rating in rating_distribution:
            rating_distribution[rating] = int((rating_distribution[rating] / review_count) * 100)
    
    # Get related courses (same category, exclude current)
    related_courses = Course.objects.filter(
        category=course.category, 
        is_active=True
    ).exclude(id=course.id)[:3]
    
    # Check if user has this course in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = request.user.wishlist.filter(course=course).exists()
    
    context = {
        'course': course,
        'modules': modules,
        'instructor': instructor,
        'reviews': reviews[:3],  # Limit to 3 initial reviews
        'review_count': review_count,
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
        'related_courses': related_courses,
        'in_wishlist': in_wishlist,
    }
    
    return render(request, 'courses-details.html', context)

def add_to_wishlist(request, course_id):
    """View to add/remove a course from user's wishlist"""
    if not request.user.is_authenticated:
        # Handle unauthenticated users (redirect to login)
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, course=course)
    
    if not created:
        # If it already existed, remove it (toggle behavior)
        wishlist_item.delete()
    
    # Redirect back to the course page
    return redirect('course_detail', slug=course.slug)

def course(request):
    course = Course.objects.all()
    context = {'course' : course}
    return render(request, 'courses.html', context)

def course_details(request, id):
    course = Course.objects.get(id = id)
    context = {'course' : course}
    return render(request, 'courses-details.html', context)

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
        country = request.POST.get('country')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate form data
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        try:
            username = email  # Using email as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create empty profile, will be updated later with course/country
            get_country = Country.objects.create(name = country)
            Profile.objects.create(user=user, country = get_country)

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

#Admin Views
def admin_dashboard(request):
    return render(request, 'school_admin/dashboard.html')

def manage_users(request):
    return render(request, 'school_admin/manage_users.html')

def courses(request):
    return render(request, 'school_admin/course_classes.html')

def curriculum(request):
    return render(request, 'school_admin/curriculum.html')

def calendar(request):
    return render(request, 'school_admin/calendar.html')

def analytics(request):
    return render(request, 'school_admin/reports.html')

def attendance(request):
    return render(request, 'school_admin/attendance.html')

def communications(request):
    return render(request, 'school_admin/communications.html')

def finance_fees(request):
    return render(request, 'school_admin/finance_fees.html')

def document_management(request):
    return render(request, 'school_admin/document_management.html')