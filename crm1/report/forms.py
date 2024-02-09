from django import forms
from .models import *
from django.shortcuts import render

from .filters import LessonPlanFilter, TopicFilter

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



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


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['name', 'faculty', 'dept', 'sem', 'topic_ids']
