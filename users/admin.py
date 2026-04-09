from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Invitation, User, UserProfile

# Register your Custom User
admin.site.register(User, UserAdmin)

# Register your other models
admin.site.register(UserProfile)
admin.site.register(Invitation)
