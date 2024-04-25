from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserModel


# forms.py

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ("email",)

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import password_validation

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email")
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error("new_password2", "The passwords do not match.")
            password_validation.validate_password(new_password1)
        return cleaned_data
from django import forms
from .models import *
from django.shortcuts import render

from .filters import LessonPlanFilter, TopicFilter


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['remarks', 'status']


class CombinedFilterForm(forms.Form):
    lesson_plan_filter = LessonPlanFilter().form
    topic_filter = TopicFilter().form

class FacultyUpdateForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    usertype = forms.CharField(max_length=50)
    contact = forms.CharField(max_length=20)
    dept = forms.CharField(max_length=50)

from django import forms

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['name', 'faculty', 'dept', 'sem', 'topic_ids']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'id_name'}),
            'faculty': forms.TextInput(attrs={'id': 'id_faculty'}),
            'dept': forms.TextInput(attrs={'id': 'id_dept'}),
            'sem': forms.TextInput(attrs={'id': 'id_sem'}),
            'topic_ids': forms.Select(attrs={'id': 'id_topic_ids'}),
            # Add more fields as needed
        }
