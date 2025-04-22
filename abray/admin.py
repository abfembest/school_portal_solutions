from django.contrib import admin
from .models import Course, Country, Profile

# Register your models here.
admin.site.register(Course)
admin.site.register(Country)
admin.site.register(Profile)