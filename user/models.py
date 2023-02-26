from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            self.set_password(self.password)
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):

    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=50,null=True, blank=True)
    # add other fields as needed
    image = models.ImageField(upload_to="media", blank=True,null=True)
    phone = models.CharField(max_length=15 ,null=True, blank=True)
    university = models.CharField(max_length=50,null=True , blank=True)
    major = models.CharField(max_length=50 ,null=True , blank=True)
    address = models.CharField(max_length=100 ,null=True , blank=True)
    date_of_birth = models.DateField(null=True , blank=True)
    GENDER_CHOICES = (('male', 'male'),('female', 'female'), )
    gender = models.CharField(max_length=20,choices= GENDER_CHOICES ,null=True , blank=True)

    def __str__(self):
        return str(self.user.username)

class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


class Teacher(User):

    base_role = User.Role.TEACHER

    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for teachers"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True )
    full_name = models.CharField(max_length=50,null=True, blank=True)
    image = models.ImageField(upload_to="media", blank=True)
    phone = models.CharField(max_length=15 ,null=True , blank=True)
    university = models.CharField(max_length=50 ,null=True , blank=True)
    major = models.CharField(max_length=50 ,null=True , blank=True)

    


@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.create(user=instance)