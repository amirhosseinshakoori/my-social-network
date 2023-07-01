from django.contrib import admin
from django.contrib.auth.models import Group , User
from .models import Profile , Tweet


class ProfileInline(admin.StackedInline):
	model = Profile
admin.site.unregister(Group)
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["Username"]
    inlines = [ProfileInline]
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Tweet)
class Profileinline(admin.StackedInline):
    model = Profile