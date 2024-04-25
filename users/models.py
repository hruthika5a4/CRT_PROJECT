from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    uname = models.CharField(default='xyz', max_length=100)
    user_type = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'), ('faculty', 'Faculty')
    ])
    contact = models.CharField(max_length=20)
    dept = models.CharField(max_length=20, choices=[
        ('civil', 'Civil'), ('mech', 'Mechanical'), ('eee', 'EEE'),
        ('ece', 'ECE'), ('cse', 'CSE'), ('ai_ds', 'AI&DS'),
        ('ds', 'DS'), ('crt', 'CRT'), ('hns', 'H&S')
    ])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_user_type_display_choices(self):
        return self._meta.get_field('user_type').choices

    def get_dept_display_choices(self):
        return self._meta.get_field('dept').choices

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(UserModel,on_delete=models.DO_NOTHING,null=True,blank=True)
    dept = models.CharField(max_length=20, choices=[
        ('civil', 'Civil'), ('mech', 'Mechanical'), ('eee', 'EEE'),
        ('ece', 'ECE'), ('cse', 'CSE'), ('ai_ds', 'AI&DS'),
        ('ds', 'DS'), ('crt', 'CRT'), ('hns', 'H&S')
    ])
    sem = models.CharField(max_length=20, choices=[
        ('1-1', 'I-I'), ('1-2', 'I-II'), ('2-1', 'II-I'),
        ('2-2', 'II-II'), ('3-1', 'III-I'), ('3-2', 'III-II'),
        ('4-1', 'IV-I'), ('4-2', 'IV-II')
    ])
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('co', 'CO'), ('ns', 'NS')], default='ns')
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.topic_name+"_"+self.dept


class LessonPlan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(UserModel, related_name='courses',on_delete=models.DO_NOTHING,null=True,blank=True)
    dept = models.CharField(max_length=20, choices=[
        ('civil', 'Civil'), ('mech', 'Mechanical'), ('eee', 'EEE'),
        ('ece', 'ECE'), ('cse', 'CSE'), ('ai_ds', 'AI&DS'),
        ('ds', 'DS'), ('crt', 'CRT'), ('hns', 'H&S')
    ])
    sem = models.CharField(max_length=20, choices=[
        ('1-1', 'I-I'), ('1-2', 'I-II'), ('2-1', 'II-I'),
        ('2-2', 'II-II'), ('3-1', 'III-I'), ('3-2', 'III-II'),
        ('4-1', 'IV-I'), ('4-2', 'IV-II')
    ])
    topic_ids = models.ManyToManyField(Topic, related_name='courses')

    def __str__(self):
        return self.sem+"_"+self.name
