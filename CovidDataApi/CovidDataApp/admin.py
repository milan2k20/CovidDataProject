from django.contrib import admin
from CovidDataApp.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'password']


admin.site.register(User, UserAdmin)
