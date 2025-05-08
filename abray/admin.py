from django.contrib import admin
from .models import Profile, Course, Country, CourseModule, Lesson, Instructor, Review, Category, CourseResource, Wishlist, Order, OrderItem

# Register your models here.
admin.site.register(Course)
admin.site.register(Country)
admin.site.register(Profile)
admin.site.register(CourseModule)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(CourseResource)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)