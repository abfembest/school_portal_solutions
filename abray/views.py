from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def course(request):
    return render(request, 'courses.html')

def course_details(request):
    return render(request, 'courses-details.html')

def course_upload(request):
    return render(request, 'course-upload.html')

def register(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'signin.html')

def password_reset(request):
    return 'Hi'