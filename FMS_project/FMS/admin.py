from django.contrib import admin
from models import School, Topic, UserProfile, Supervisor, Project, Student, Application
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('user.first_name'+" "+'user.first_name'+" "+'user.id',)}

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title'+" "+'id',)}

admin.site.register(School)
admin.site.register(Topic)
admin.site.register(UserProfile)
admin.site.register(Supervisor)
admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Application)