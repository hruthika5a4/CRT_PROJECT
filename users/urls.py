from django.urls import path

from .views import *
from . import views

urlpatterns = [

    path('login/', login_view, name='login'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('password_reset/', password_reset, name='password_reset'),
    path('success_reset/', success_reset, name='success_reset'),

    path('admin/dashboard/<str:email>/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('update-topic1/<int:topic_id>/', views.update_topic1, name='update_topic'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('faculty/<str:email>/', views.faculty_dashboard, name='faculty_dashboard'),
    path('lessonplan/', views.lessonplan, name='lsp'),
    path('faculty-list/', views.faculty_list, name='faculty_list'),
    path('update-faculty/<str:email>/', views.update_faculty, name='update_user'),
    path('delete-faculty/<str:email>/', views.delete_faculty, name='delete_faculty'),

    path('add-faculty/', views.add_faculty, name='add_faculty'),



     path('topic-list/', views.topic_list, name='topic_list'),
     path('update-topic/<int:topic_id>/', views.update_topic, name='update_topic'),
      path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
      path('add-topic/', views.add_topic, name='add_topic'),

     path('add-lesson-plan/', views.add_lesson_plan, name='add_lesson_plan'),
     path('fetch-topics/', views.fetch_topics, name='fetch_topics'),
      path('lesson-plans/', views.lesson_plan_list, name='lesson_plan_list'),
      path('lesson-plans/delete/<int:lesson_plan_id>/', views.delete_lesson_plan, name='delete_lesson_plan'),
      path('report/add-topic/', views.add_topic, name='add_topic'),




       path('get-user-ids/', views.get_user_ids, name='get_user_ids'),
path('topic-faculty-view/<str:user_email>/', views.topic_faculty_view, name='topic_faculty_view'),



     path('faculty-lesson-plans/<str:user_email>/', views.faculty_lesson_plans, name='lsp-faculty-view'),





     

     
     
      path('import_page/', views.import_data_page, name='import_data_page'),

     
      path('import/', views.import_topics_from_file, name='import_topics'),


     path('profile/<str:user_email>/', views.user_profile, name='user_profile'),

     path('report_table/', views.report_table, name='report_table'),

]







