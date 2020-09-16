from django.contrib import admin

# Register your models here.
from app2 import models
from app2.models import Student,InClass

admin.site.register(models.Student)
admin.site.register(models.InClass)
