from django.shortcuts import redirect, render,HttpResponse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import StudentProfile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.

def student_login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= authenticate(username = username, password = password)

            if user is not None:
                login(request, user)
                
                if request.user.role in ["ADMIN","TEACHER"]:
                    return HttpResponse("You are not a student!!")
                else:
                    return redirect("student_profile")
            else:
                alert = True
                return render(request, "user/student/student_login.html", {'alert':alert , 'form':form})

    return render(request, "user/student/student_login.html",{'form':form})


@login_required(login_url = '/student_login')
def student_profile(request ):
    return render(request, "user/student/student_profile.html")


class StudentProfileUpdateView (UpdateView):
    model = StudentProfile
    login_required = True
    fields = ['full_name', 'student_id' ,'address', 'image','phone','university','major', 'date_of_birth','gender' ]
    template_name= "user/student/studentprofile_update_form.html"
    success_url = reverse_lazy("student_profile")

def Logout(request):
    logout(request)
    return redirect ("student_login")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "user/change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "user/change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "user/change_password.html")

