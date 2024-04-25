import django_filters

from .models import *

class LessonPlanFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Course Name')

    class Meta:
        model=LessonPlan
        fields = ['faculty','name','dept','sem']






class LessonPlanFilter1(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Course Name')

    class Meta:
        model=LessonPlan
        fields = ['name','dept','sem']




class TopicFilter1(django_filters.FilterSet):
    class Meta:
        model=Topic
        fields = ['status']





class LessonPlanFilter2(django_filters.FilterSet):

    Course_Name = django_filters.ModelChoiceFilter(
        queryset=LessonPlan.objects.all(),
        field_name='name',
        to_field_name='name',
        label='Course Name',
        
    )

    class Meta:
        model = LessonPlan
        fields = ['Course_Name']

class TopicFilter(django_filters.FilterSet):
    topic_name = django_filters.CharFilter(lookup_expr='icontains', label='Topic Name')

    class Meta:
        model=Topic
        fields = ['topic_name','dept','sem','status']


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






class TopicFilter5(django_filters.FilterSet):
    faculty_uname = django_filters.ModelChoiceFilter(
        queryset=UserModel.objects.values_list('email', flat=True).distinct(),
        empty_label='Select Faculty',
        label='Faculty Email',
        field_name='faculty__email'  # specify the related field name
    )

    class Meta:
        model = Topic
        fields = ['faculty_uname', 'sem', 'dept']