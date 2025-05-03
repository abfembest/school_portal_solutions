from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')  # Instructor
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)      # Enrolled students

    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50, unique=True)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='course_images/')
    category = models.CharField(max_length=100)
    # start_date = models.DateField(null=True)
    # end_date = models.DateField()
    # enrollment_limit = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.course_code})"

class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"