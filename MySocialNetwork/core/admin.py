from django.contrib import admin
from django.contrib.auth.models import Group , User
from .models import Profile

admin.site.unregister(Group)
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["Username"]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

class Profileinline(admin.StackedInline):
    model = Profile