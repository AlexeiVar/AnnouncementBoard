from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
# Регистрирую кастом юзера, согласно документации
admin.site.register(CustomUser, UserAdmin)

