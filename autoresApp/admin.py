from django.contrib import admin
from autoresApp.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...
