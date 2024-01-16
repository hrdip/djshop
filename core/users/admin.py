from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User

# Register your models here.
class DjshopUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'verified_email')

 
admin.site.register(User, DjshopUserAdmin)