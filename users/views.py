from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *

from django.contrib.auth import get_user_model
from datetime import datetime


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'admin':
                    print("admin")
                    return redirect('admin_dashboard',email=username)  # Redirect to admin dashboard

                elif user.user_type == 'faculty':
                    print("faculty")
                    return redirect('faculty_dashboard',email=username)  # Redirect to faculty dashboard
                else:
                    print("home")
                    return redirect('home')  # Default redirect
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



User = get_user_model()

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password1']
            User = get_user_model()  # Get the custom user model
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Handle case where email doesn't exist
                pass
            else:
                user.set_password(new_password)
                user.save()
                return redirect('success_reset')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})


def success_reset(request):
    return render(request, 'success_reset.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # Use your custom form here
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"



from django.shortcuts import render
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import UserModel
from .forms import LoginForm, TopicForm ,FacultyUpdateForm

from .filters import *

from django.http import JsonResponse
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from .models import UserModel, LessonPlan, Topic
from .forms import LoginForm,LessonPlanForm

from django.http import HttpResponse, HttpResponseBadRequest

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse


from django.db.models import Count



def get_user_ids(request):
    try:
        # Fetch all user IDs
        user_ids = UserModel.objects.values_list('id', flat=True)
        return JsonResponse(list(user_ids), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def fetch_topics(request):
    # Get parameters from the request
    selected_faculty = request.GET.get('faculty', None)
    selected_sem = request.GET.get('sem', None)
    selected_dept = request.GET.get('dept', None)
    print(selected_sem)
    print(selected_dept)
    print(selected_faculty)

    # Query topics based on selected_sem, selected_dept, and selected_faculty
    if selected_sem and selected_dept and selected_faculty:
        # Check if selected_faculty is an email or an ID
        if selected_faculty.isdigit():
            # If selected_faculty can be converted to an integer, it's likely an ID
            topics = Topic.objects.filter(sem=selected_sem, dept=selected_dept, faculty_id=selected_faculty).distinct()
        else:
            # If selected_faculty is not an integer, it's likely an email
            topics = Topic.objects.filter(sem=selected_sem, dept=selected_dept, faculty__email=selected_faculty).distinct()

        # Create a list of topic data
        topics_data = [{'id': topic.topic_id, 'name': topic.topic_name} for topic in topics]
        return JsonResponse(topics_data, safe=False)
    else:
        # Return an empty list if sem or dept is not provided
        return JsonResponse([], safe=False)


def lesson_plan_list(request):
    # Retrieve all lesson plans from the database
    lesson_plans = LessonPlan.objects.all()
    lesson_plan_form = LessonPlanForm(request.POST or None)
    lesson_plan_filter = LessonPlanFilter(request.GET, queryset=lesson_plans) 
    lesson_plans=lesson_plan_filter.qs # Apply the filter
    context={
        'lesson_plans':lesson_plans,
        'lesson_plan_form':lesson_plan_form,
        'lesson_plan_filter': lesson_plan_filter,  # Pass the filter to the context
    }
    # Pass the retrieved lesson plans to the template
    return render(request, 'report/lesson_plan_list.html', context)

def delete_lesson_plan(request, lesson_plan_id):
    lesson_plan = get_object_or_404(LessonPlan, id=lesson_plan_id)
    lesson_plan.delete()
    return redirect('lesson_plan_list')



def update_topic1(request, topic_id):
    print("-------------------------")
    if request.method == 'POST':
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        print(status)
        print(remarks)

        try:
            topic = Topic.objects.get(pk=topic_id)
            topic.status = status
            topic.remarks = remarks
            topic.save()
            return JsonResponse({'success': True})
        except Topic.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topic not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             try:
#                 user = UserModel.objects.get(email=email, password=password)
                
#                 if user.user_type == 'faculty':
#                     # If the user is a faculty, redirect to the faculty dashboard
#                     return redirect('faculty_dashboard', email=email)
#                 elif user.user_type == 'admin':
#                     # If the user is an admin, redirect to the admin dashboard
#                     return redirect('admin_dashboard', email=email)

#             except UserModel.DoesNotExist:
#                 return render(request, 'report/login.html', {'form': form, 'error': 'Invalid email or password'})

#     else:
#         form = LoginForm()

#     return render(request, 'report/login.html', {'form': form, 'error': ''})


def faculty_dashboard(request, email):
    # Retrieve the faculty based on the provided email
    faculty = get_object_or_404(UserModel, email=email)

    # Retrieve all Lesson Plans associated with the faculty
    all_lesson_plans = LessonPlan.objects.filter(faculty=faculty)
    # Apply LessonPlanFilter if needed

    # Count total Lesson Plans
    total_lesson_plans_count = all_lesson_plans.count()

    # Initialize counters
    ns_topics_count = 0
    total_topics_count = 0

    myFilter = LessonPlanFilter1(request.GET, queryset=all_lesson_plans)
    filtered_lesson_plans = myFilter.qs

    print(all_lesson_plans)
    print(filtered_lesson_plans )

    topic_filter = TopicFilter1(request.GET, queryset=filtered_lesson_plans)


    # Fetch details for each Lesson Plan
    lesson_plan_details = []
    
    for lesson_plan in filtered_lesson_plans:
        name = lesson_plan.name
        dept = lesson_plan.dept
        sem = lesson_plan.sem

        # Fetch all topics for the current Lesson Plan
        topics_for_plan = lesson_plan.topic_ids.all()

        
        topic_filter = TopicFilter1(request.GET, queryset=topics_for_plan)

        topic_filter1=topic_filter.qs

        # Fetch details for each Topic using list comprehension
        topic_details = []
        for topic in topic_filter1:
            topic_details.append({
                'topic_id': topic.topic_id,
                'topic_name': topic.topic_name,
                'dept': topic.dept,
                'sem': topic.sem,
                'target_date': topic.target_date,
                'status': topic.status,
                'remarks': topic.remarks,
            })

        # Count 'ns' topics
        ns_topics_count += sum(1 for topic in topics_for_plan if topic.status == 'ns')
        
        # Update total topics count
        total_topics_count += len(topics_for_plan)

        # Append details for the current Lesson Plan to the list
        lesson_plan_details.append({
            'name': name,
            'dept': dept,
            'sem': sem,
            'topics': topic_details,
        })

    context = {
        'email': email,
        'faculty': faculty,
        'lesson_plan_details': lesson_plan_details,
        'total_lesson_plans_count': total_lesson_plans_count,
        'total_topics_count': total_topics_count,
        'ns_topics_count': ns_topics_count,
        'cn_topics_count': total_topics_count - ns_topics_count,
        'myFilter': myFilter,  # Pass the filter to the template context if needed
        'topic_filter': topic_filter, 
    }
    print(faculty)
    print(email)
    return render(request, 'report/faculty_dashboard.html', context)


def lessonPlanForm(request):
    form = LessonPlanForm()
    return render(request, 'report/faculty_lsp_view.html', {'form': form})


def admin_dashboard(request, email):
    # Retrieve all Lesson Plans
    all_lesson_plans = LessonPlan.objects.all()
    filtered_Topics=None
    # Use the LessonPlanFilter to filter lesson plans based on the request.GET parameters
    myFilter = LessonPlanFilter1(request.GET, queryset=all_lesson_plans)
    filtered_lesson_plans = myFilter.qs
    filtered_Topics = TopicFilter1(request.GET, queryset=filtered_lesson_plans)
        
    # Count total Lesson Plans, Topics, and Users after filtering
    total_lesson_plans_count = filtered_lesson_plans.count()
    total_topics_count = Topic.objects.count()
    total_users_count = UserModel.objects.count()

    # Fetch details for each Lesson Plan
    lesson_plan_details = []
    for lesson_plan in filtered_lesson_plans:
        name = lesson_plan.name
        faculty = lesson_plan.faculty
        dept = lesson_plan.dept
        sem = lesson_plan.sem

        # Fetch all topics for the current Lesson Plan
        topics_for_plan = lesson_plan.topic_ids.all()

        # Use the TopicFilter to filter topics based on the request.GET parameters
        filtered_Topics = TopicFilter1(request.GET, queryset=topics_for_plan)
        filtered_Topics1 = filtered_Topics.qs

        # Fetch details for each Topic
        topic_details = []
        for topic in filtered_Topics1:
            topic_details.append({
                'topic_id': topic.topic_id,
                'topic_name': topic.topic_name,
                'dept': topic.dept,
                'sem': topic.sem,
                'target_date': topic.target_date,
                'status': topic.status,
                'remarks': topic.remarks,
            })

        # Append details for the current Lesson Plan to the list
        lesson_plan_details.append({
            'name': name,
            'faculty': faculty,
            'dept': dept,
            'sem': sem,
            'topics': topic_details,
        })

    context = {
        'email':email,
        'lesson_plan_details': lesson_plan_details,
        'total_lesson_plans_count': total_lesson_plans_count,
        'total_topics_count': total_topics_count,
        'total_users_count': total_users_count,
        'myFilter': myFilter,  # Pass the filter to the template context
        'filtered_Topics': filtered_Topics,
    }
    return render(request, 'report/admin_dashboard.html', context)


def home(request):
    return render(request, 'report/admin_dashboard.html')

def faculty(request):
    return render(request,'report/faculty_dashboard.html')

def lessonplan(request):
    return render(request,'report/lessonplan.html')





def faculty_list(request):
    faculty_members = UserModel.objects.all()
    return render(request, 'report/faculty_list.html', {'faculty_members': faculty_members})

from django.middleware.csrf import get_token


import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def update_faculty(request, email):
    faculty_member = get_object_or_404(UserModel, email=email)

    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                # If data is sent as JSON
                data = json.loads(request.body)
                user_type = data.get('user_type')
                contact = data.get('contact')
                dept = data.get('dept')
                password = data.get('password')
            else:
                # If data is sent as form data
                user_type = request.POST.get('user_type')
                contact = request.POST.get('contact')
                dept = request.POST.get('dept')
                password = request.POST.get('password')

            # Update the faculty_member fields based on the form data
            faculty_member.user_type = user_type
            faculty_member.contact = contact
            faculty_member.dept = dept
            # Update password only if provided
            if password:
                faculty_member.password=password

            faculty_member.save()

            return JsonResponse({'message': 'Faculty information updated successfully'})
        except KeyError:
            # Handle missing key in form data or JSON
            return JsonResponse({'error': 'Missing key in data'}, status=400)

    return JsonResponse({'message': 'Error updating faculty information'}, status=400)



def update_user(request, email):
    user = get_object_or_404(UserModel, email=email)

    if request.method == 'POST':
        try:
            user_type = request.POST.get('user_type')
            contact = request.POST.get('contact')
            dept = request.POST.get('dept')

            # Update the user fields based on the form data
            user.user_type = user_type
            user.contact = contact
            user.dept = dept

            user.save()

            return JsonResponse({'message': 'User information updated successfully'})
        except KeyError:
            # Handle missing key in POST data
            return JsonResponse({'error': 'Missing key in POST data'}, status=400)

    return JsonResponse({'message': 'Error updating user information'}, status=400)






def delete_faculty(request, email):
    faculty_member = get_object_or_404(UserModel, email=email)
    print(faculty_member)

    if request.method == 'POST':
        try:
            # Delete the faculty member
            faculty_member.delete()

            return JsonResponse({'message': 'Faculty member deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting faculty member: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)





def add_faculty(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_type = request.POST.get('user_type')
            contact = request.POST.get('contact')
            dept = request.POST.get('dept')

            # Check if the email already exists in the database
            if UserModel.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            # Create a new faculty member
            new_faculty = UserModel(email=email, password=password, user_type=user_type, contact=contact, dept=dept)
            new_faculty.save()

            return JsonResponse({'message': 'Faculty information added successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error adding faculty information: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=400)







def topic_list(request):
    topics = Topic.objects.all()
    faculty_list = UserModel.objects.all()
    # Apply filters based on request.GET parameters
    topic_filter = TopicFilter(request.GET, queryset=topics)
    filtered_topics = topic_filter.qs

    return render(request, 'report/topic_list.html', {'topics': filtered_topics, 'filter': topic_filter,'faculty_list': faculty_list,})

from django.utils.dateparse import parse_date

def update_topic(request, topic_id):
    topic = get_object_or_404(Topic, topic_id=topic_id)

    if request.method == 'POST':
        # Update4 topic data based on form submission
       
        topic.dept = request.POST.get('dept')
        topic.sem = request.POST.get('sem')

        # Validate and handle the date field
        target_date_str = request.POST.get('target_date')
        if target_date_str:
            try:
                topic.target_date = parse_date(target_date_str)
            except ValidationError:
                # Handle invalid date format
                # You can customize this part based on your needs
                return HttpResponseBadRequest("Invalid date format for 'target_date'")
        else:
            topic.target_date = None

        topic.status = request.POST.get('status')
        topic.remarks = request.POST.get('remarks')

        topic.save()

        # Return a JSON response on success
        return JsonResponse({'message': 'Topic information updated successfully!'})

    # Handle other cases (GET request or form rendering)
    return render(request, 'report/update_topic.html', {'topic': topic})




def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, topic_id=topic_id)

    if request.method == 'POST':
        try:
            # Delete the topic
            topic.delete()
            return JsonResponse({'message': 'Topic deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting topic: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)





def add_topic(request):
    try:
        # Retrieve data from the POST request
        data = request.POST
        print(data)
        # Convert the 'None' string to actual None
        target_date_str = data.get('target_date')
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date() if target_date_str and target_date_str != 'None' else None


        
        faculty_email = data['faculty']
        faculty_instance = UserModel.objects.get(email=faculty_email)  # Adjust this based on your actual User model field


        # Create a new topic instance
        new_topic = Topic.objects.create(
            topic_name=data.get('topic_name'),
            faculty=faculty_instance,
            dept=data.get('dept'),
            sem=data.get('sem'),
            target_date=target_date,
            status=data.get('status'),
            remarks=data.get('remarks'),
            
        )

        return JsonResponse({'message': 'Topic added successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Error adding topic: {str(e)}'}, status=500)
    




def add_lesson_plan(request):
    try:
        # Retrieve data from the POST request
        data = request.POST
        print("hi")
        print(data)
        # Get the UserModel instance based on faculty_id or faculty_email
        faculty_identifier = data.get('faculty')
        if faculty_identifier.isdigit():
            # If faculty_identifier can be converted to an integer, it's likely an ID
            faculty_instance = UserModel.objects.get(id=faculty_identifier)
        else:
            # If faculty_identifier is not an integer, it's likely an email
            faculty_instance = UserModel.objects.get(email=faculty_identifier)

        print(faculty_instance)
        # Create a new LessonPlan instance
        new_lesson_plan = LessonPlan.objects.create(
            name=data.get('name'),
            faculty=faculty_instance,
            dept=data.get('dept'),
            sem=data.get('sem'),
        )

        # Assign topics to the lesson plan
        topic_ids = data.getlist('topic_ids')
        new_lesson_plan.topic_ids.set(topic_ids)

        return JsonResponse({'message': 'Lesson Plan added successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Error adding Lesson Plan: {str(e)}'}, status=500)




def topic_faculty_view(request, user_email):
    # Step 1: Retrieve the Faculty object based on the provided user_email
    faculty = get_object_or_404(UserModel, email=user_email)
    faculty_list = UserModel.objects.all()
    # Step 2: Get the lesson plans associated with the faculty
    lesson_plans = LessonPlan.objects.filter(faculty=faculty)


    myFilter = LessonPlanFilter2(request.GET, queryset=lesson_plans)
    filtered_lesson_plans = myFilter.qs
    filtered_Topics = TopicFilter1(request.GET, queryset=filtered_lesson_plans)
        


    # Step 3: For each lesson plan, retrieve data fields of each topic
    topic_data = []
    for lesson_plan in filtered_lesson_plans:
        topics_for_lesson_plan = lesson_plan.topic_ids.all()
        filtered_Topics = TopicFilter(request.GET, queryset=topics_for_lesson_plan)
        filtered_Topics1 = filtered_Topics.qs
        for topic in filtered_Topics1:
            # Include all fields from the Topic model
            topic_data.append({
                'lesson_plan': lesson_plan,
                'topic_id': topic.topic_id,
                'topic_name': topic.topic_name,
                'dept': topic.dept,
                'sem': topic.sem,
                'target_date': topic.target_date,
                'status': topic.status,
                'remarks': topic.remarks,
                # Add more fields as needed
            })

    # Pass the data to the template
    context = {
        'faculty': faculty,
        'topic_data': topic_data,
        'myFilter':myFilter,
        'filtered_Topics':filtered_Topics,
        'faculty_list':faculty_list,
    }

    return render(request, 'report/topic_faculty_view.html', context)



def faculty_lesson_plans(request, user_email):
    # Step 1: Retrieve the Faculty object based on the provided user_email
    faculty = get_object_or_404(UserModel, email=user_email)

    # Step 2: Get the lesson plans associated with the faculty
    lesson_plans = LessonPlan.objects.filter(faculty=faculty)
    print(lesson_plans)

    lesson_plan_filter = LessonPlanFilter1(request.GET, queryset=lesson_plans)
    lesson_plans = lesson_plan_filter.qs


    # Step 3: For each lesson plan, retrieve data fields of each topic
    lesson_plans_data = []
    for lesson_plan in lesson_plans:
        topics_for_lesson_plan = lesson_plan.topic_ids.all()
        lesson_plan_data = {
            'id': lesson_plan.id,
            'name': lesson_plan.name,
            'faculty': lesson_plan.faculty.uname,
            'dept': lesson_plan.dept,
            'sem': lesson_plan.sem,
            'topics': [{'topic_name': topic.topic_name} for topic in topics_for_lesson_plan],
        }
        lesson_plans_data.append(lesson_plan_data)
    lesson_plan_form = LessonPlanForm()
    # Pass the data to the template
    context = {
        'email':user_email,
        'faculty': faculty,
        'lesson_plans_data': lesson_plans_data,
        'lesson_plan_form': lesson_plan_form,
        'lesson_plan_filter': lesson_plan_filter,
    }

    return render(request, 'report/faculty_lsp_view.html', context)












def import_topics_from_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        # Assuming the file contains space-separated values for each field
        content = file.read().decode('utf-8')
        lines = content.split('\n')

        for line in lines:
            values = line.split()

            # Assuming the order of values in the line corresponds to the order of fields in the model
            topic_name = values[0]
            dept = values[1]
            sem = values[2]
            target_date = values[3] if len(values) > 3 else None
            status = values[4] if len(values) > 4 else 'ns'
            remarks = ' '.join(values[5:]) if len(values) > 5 else None

            # Create instances of Topic with the data from the file
            Topic.objects.create(
                topic_name=topic_name,
                dept=dept,
                sem=sem,
                target_date=target_date,
                status=status,
                remarks=remarks,
            )

        return render(request, 'report/success.html')

    return render(request, 'report/update_data.html')






def import_data_page(request):
    return render(request, 'report/import_data.html')






def user_profile(request, user_email):
    try:
        # Retrieve the user based on the provided email
        user = UserModel.objects.get(email=user_email)

        # Get the count of lesson plans related to the user
        lesson_plan_count = LessonPlan.objects.filter(faculty=user).count()

        # Get the count of topics related to the user
        topic_count = Topic.objects.filter(faculty=user).count()

        # Pass the user details and counts to the template
        context = {
            'user': user,
            'lesson_plan_count': lesson_plan_count,
            'topic_count': topic_count,
        }

        return render(request, 'report/profile.html', context)

    except UserModel.DoesNotExist:
        # Handle the case where the user with the specified email is not found
        # You can customize this part based on your application's requirements
        return render(request, 'report/user_not_found.html') 
    




def report_table(request):
    # Get all topics initially
    topics = Topic.objects.all()
    myFilter = TopicFilter5(request.GET, queryset=topics)
    # Check if there are any filters in the request
    if request.GET:
        # Apply filtering if there are GET parameters
       
        topics = myFilter.qs
    else:
        # If no filters, myFilter will be None
        topics = None
        

    # Pass the topics and the filter to the template
    context = {
        'topics': topics,
        'myFilter': myFilter,
    }

    return render(request, 'report/report_table.html', context)