from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile, Friend, ChatMessage

# Register your models here.
def log_in_as_user(modeladmin, request, queryset):
    # Assuming you have a single user selected, otherwise, you can modify the logic accordingly
    selected_user = queryset.first()
    # Log in as the selected user
    user = User.objects.get(username=selected_user.username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the authentication backend
    login(request, user)

log_in_as_user.short_description = "Log in as selected user"

class CustomUserAdmin(UserAdmin):
    actions = [log_in_as_user]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register([Profile, Friend, ChatMessage])