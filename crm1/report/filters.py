import django_filters

from .models import *

class LessonPlanFilter(django_filters.FilterSet):
    class Meta:
        model=LessonPlan
        fields = ['faculty','dept','sem','name']


class LessonPlanFilter1(django_filters.FilterSet):
    class Meta:
        model=LessonPlan
        fields = ['name','dept','sem']




class TopicFilter(django_filters.FilterSet):
    class Meta:
        model=Topic
        fields = ['topic_id','topic_name','faculty','dept','sem','status']


class LessonPlanFilter_admin(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Lesson Plan Name')
    faculty = django_filters.CharFilter(lookup_expr='icontains', label='Faculty')
    sem = django_filters.CharFilter(lookup_expr='icontains', label='Semester')
    dept = django_filters.CharFilter(lookup_expr='icontains', label='Department')

    class Meta:
        model = LessonPlan
        fields = ['name', 'faculty', 'sem', 'dept']

class TopicFilter_admin(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains', label='Topic Status')
    remarks = django_filters.CharFilter(lookup_expr='icontains', label='Remarks')

    class Meta:
        model = Topic
        fields = ['status', 'remarks']

