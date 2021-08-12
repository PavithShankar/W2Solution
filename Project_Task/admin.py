from django.contrib import admin
from .models import User, Skill

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    fields = ['firstname', 'lastname', 'email', 'password']


class SkillAdmin(admin.ModelAdmin):
    fields = ['employeeinfo', 'skillname', 'percentage']


admin.site.register(User, UserAdmin)

admin.site.register(Skill, SkillAdmin)
