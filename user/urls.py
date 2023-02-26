from django.urls import path
from . import views
 
urlpatterns = [
    path("student_login/", views.student_login, name="student_login"),
    path("student_profile/", views.student_profile, name="student_profile"),
    path("update_student_profile/<int:pk>", views.StudentProfileUpdateView.as_view(), name="update_student_profile"),
    path("logout/", views.Logout, name="logout"),
    path("change_password/", views.change_password, name="change_password"),

]