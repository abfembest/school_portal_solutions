from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def course(request):
    return render(request, 'course.html')

def register(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'signin.html')

def password_reset(request):
    return 'Hi'