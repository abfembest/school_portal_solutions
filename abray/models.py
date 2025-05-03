from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Course(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    # Basic Course Info
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    
    # Category and Difficulty
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    
    # Relationships
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)
    
    # Course Metadata
    duration = models.CharField(max_length=100)  # e.g., "8 weeks"
    total_hours = models.PositiveIntegerField(default=0)  # Total video hours
    total_lessons = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField(default=0)
    
    # Additional Content
    what_will_learn = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    
    # Course Resources
    resources_count = models.PositiveIntegerField(default=0)
    exercises_count = models.PositiveIntegerField(default=0)
    
    # Course Status
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateField(default=timezone.now)
    
    # Enrollment
    enrolled_students_count = models.PositiveIntegerField(default=0)
    
    # Language
    language = models.CharField(max_length=50, default='English')
    
    # Coupon
    has_coupon = models.BooleanField(default=False)
    coupon_expiry = models.DateTimeField(null=True, blank=True)
    
    # Mobile and TV access
    has_mobile_access = models.BooleanField(default=True)
    has_tv_access = models.BooleanField(default=True)
    has_lifetime_access = models.BooleanField(default=True)
    has_certificate = models.BooleanField(default=True)
    has_instructor_support = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.course_code})"
    
    def save(self, *args, **kwargs):
        # Calculate discount percentage if original_price is provided
        if self.original_price and self.price < self.original_price:
            self.discount_percentage = int(((self.original_price - self.price) / self.original_price) * 100)
        
        # Auto-update counts
        if self.id:
            self.total_modules = self.modules.count()
            lesson_count = 0
            for module in self.modules.all():
                lesson_count += module.lessons.count()
            self.total_lessons = lesson_count
            self.enrolled_students_count = self.students.count()
        
        super(Course, self).save(*args, **kwargs)

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=50)  # e.g., "3 hours"
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"

class Lesson(models.Model):
    LESSON_TYPE_CHOICES = (
        ('video', 'Video Lesson'),
        ('text', 'Text Lesson'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('code', 'Coding Exercise'),
    )
    
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='video')
    duration = models.CharField(max_length=50)  # e.g., "45 min"
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - Lesson {self.order}: {self.title}"

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='instructor_images/', null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)  # e.g., "AI Research Scientist"
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    students_count = models.PositiveIntegerField(default=0)
    courses_count = models.PositiveIntegerField(default=0)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s review on {self.course.title}"

class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class CourseResource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('code', 'Code File'),
        ('zip', 'ZIP Archive'),
        ('other', 'Other')
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file = models.FileField(upload_to='course_resources/')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s wishlist - {self.course.title}"