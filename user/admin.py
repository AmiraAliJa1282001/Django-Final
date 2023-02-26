from django.contrib import admin

# Register your models here.
from .models import Student ,StudentProfile , Teacher , TeacherProfile, User

class StudentAdmin(admin.ModelAdmin):
    model = Student
    fields = ["username", "password" ,"email"] 

class TeacherAdmin(admin.ModelAdmin):
    model = Student
    fields = ["username", "password" ,"email"] 

admin.site.register(User )
admin.site.register(Student,StudentAdmin )
admin.site.register(StudentProfile)
admin.site.register(Teacher ,TeacherAdmin)
admin.site.register(TeacherProfile)
