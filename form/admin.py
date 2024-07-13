from django.contrib import admin
from .models import Userprofile, UserPhotos

class UserPhotosInline(admin.TabularInline):
    model = UserPhotos
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserPhotosInline]

admin.site.register(Userprofile, UserProfileAdmin)
admin.site.register(UserPhotos)
