from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
import requests
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from .forms import *
from django.forms.widgets import HiddenInput
from django.http import HttpResponse
from .models import *
from django.db.models.functions import Lower
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def notification_page(request):
    return render(request,'home/notificationpage.html')

def schedule_page(request):
    my_user = TutoringUser.objects.filter(user=request.user).first()
    # print(my_user.is_tutor)
    if my_user.is_tutor == True:
        if request.method == 'GET':
            # request_list = TutorRequest.objects.get(request_user=request.user.username)
            request_list = TutorRequest.objects.filter(tutor=request.user)
            # print(request_list,'udgwgduwgf')
            return render(request,'home/schedulepage.html', {'request_list' : request_list})
    return render(request,'home/schedulepage.html')

def profile_page(request):
    tutor_user = TutoringUser.objects.filter(user=request.user).first();
    classes = tutor_user.classes
    new_classes = []
    for course in classes:
        course_parts = course.split()
        new_course = " ".join(course_parts[1:])
        new_classes.append(new_course)
    return render(request,'home/profilepage.html', {'courses': new_classes})

def search_tutors(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_id')
        tutor = TutoringUser.objects.filter(id=tutor_id).first()
        if tutor:
            session_date_time = request.POST.get('session_date')
            date_time = session_date_time.split()
            session_date = date_time[0]
            session_time = date_time[1]
            session_duration = request.POST.get('session_size')
            description = request.POST.get('description')
            student = request.user
         
            tutor_request = TutorRequest.objects.create(
                student=student,
                tutor=tutor.user,
                session_date=session_date,
                session_time=session_time,
                duration = session_duration,
                description=description,
                status='pending'
            )
            # print(tutor_request)
            tutor_request.save()
            return redirect('/requestlist')  # replace with the appropriate URL for the student dashboard
        else:
            # print('failed')
            return render(request, 'home/tutorsearch.html', {'error': 'Tutor not found'})
    elif request.method == 'GET':
        input = request.GET.get('input')
        if input is None:
            return render(request, 'home/tutorsearch.html', {'tutor_list': []})
        else:
            tutor_list = TutoringUser.objects.filter(
                Q(full_name__icontains=input) | Q(pay_rate__icontains=input) | Q(major__icontains=input) | Q(classes__icontains=input)
            )
            return render(request, 'home/tutorsearch.html', {'tutor_list': tutor_list})
    return render(request,'home/tutorsearch.html')

def view_requests(request):
    my_user = TutoringUser.objects.filter(user=request.user).first()
    # print(my_user.is_tutor)
    if my_user.is_tutor == True:
        if request.method == 'GET':
            # request_list = TutorRequest.objects.get(request_user=request.user.username)
            request_list = TutorRequest.objects.filter(tutor=request.user)
            # print(request_list,'udgwgduwgf')
            return render(request,'home/requestIndex.html', {'request_list' : request_list})
        
        if request.method == 'POST':
            request_id = request.POST.get('request_id')
            # print(request_id)
            status = request.POST.get('status')
            try:
                tutor_request = TutorRequest.objects.get(id=request_id)
                # Update the status of the tutor_request
                tutor_request.status = status
                tutor_request.save() 
                # print(tutor_request.status)
                return redirect("/requestlist")  # Redirect to the request list page after successful update
            except TutorRequest.DoesNotExist:
                # print('pass')
                pass  # Handle case where request_id does not exist
                # print('pass')
    elif my_user.is_tutor == False:
        if request.method == 'GET':
            # request_list = TutorRequest.objects.get(request_user=request.user.username)
            request_list = TutorRequest.objects.filter(student=request.user)
            # print(request_list,'udgwgduwgf')
            return render(request,'home/requestIndex.html', {'request_list' : request_list})
        
        if request.method == 'PUT':
            request_id = request.POST.get('request_id')
            status = request.POST.get('status')
            try:
                tutor_request = TutorRequest.objects.get(id=request_id)
                # Update the status of the tutor_request
                tutor_request.status = status
                tutor_request.save()
                return redirect(request,'home/requestIndex.html')  # Redirect to the request list page after successful update
            except TutorRequest.DoesNotExist:
                pass  # Handle case where request_id does not exist
                # print('pass')

def tutor_profile(request, tutor_id):
    tutor_user = get_object_or_404(User, id=tutor_id)
    tutor = get_object_or_404(TutoringUser, user=tutor_user)
    classes = tutor.classes
    tutor_classes = []
    for course in classes:
        course_parts = course.split()
        new_course = " ".join(course_parts[1:])
        tutor_classes.append(new_course)
    return render(request, 'home/viewtutorprofile.html', {'tutoring_user': tutor, 'classes': tutor_classes})

def search_courses(request):
    try:
        tutoring_user = request.user.tutoringuser
        if request.method == 'GET':
            # input = request.GET.get('search-input')
            # class_num = ""
            # subject = ""
            # course_code = ""
            # title = ""
            # instr = ""
            class_num = request.GET.get('class-number')
            subject = request.GET.get('subject')
            course_code = request.GET.get('course-code')
            title = request.GET.get('title')
            instr = request.GET.get('instructor')
            # print(title)
            if class_num == "":
                nquery = ""
            else:
                try:
                    int(class_num)
                except:
                    return render(request, 'home/courses.html', {'courses': []})
                nquery = "&class_nbr=" + class_num
            
            if subject is None:
                squery = ""
            else: 
                squery = "&subject=" + subject

            if course_code is None:
                cquery = ""
            else:
                cquery = "&catalog_nbr=" + course_code

            if title is None:
                tquery = ""
            else:
                tquery = "&keyword=" + title

            if instr is None:
                iquery = ""
            else:
                iquery = "&instructor_name=" + instr
            
            # print(nquery)
            # print(tquery)
            # print(len(nquery+squery+cquery+tquery+iquery))
            
            # if not isinstance(class_num, int):
            #     return render(request, 'home/courses.html', {'courses': []})
            if len(nquery+squery+cquery+tquery+iquery) == 0:
                return render(request, 'home/courses.html', {'courses': []})
            else:
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=1{nquery}{squery}{cquery}{tquery}{iquery}'
                r = requests.get(url)
                # print(url)
                courses = r.json()
                courses1 = []
                course_descrs = []
                unique_courses = []

                for course in courses:
                    # print(course)
                    if class_num == course['class_nbr']:
                        courses1.append(course)
                    elif subject == course['subject']:
                        courses1.append(course)
                    elif course_code == course['catalog_nbr']:
                        courses1.append(course)
                    elif title in course['descr']:
                        courses1.append(course)
                    elif instr in course['meetings'][0]['instructor']:
                        courses1.append(course)

                for course in courses1:
                    class_label = course['subject']+" "+course['catalog_nbr']+" "+course['descr']
                    if course['descr'] not in course_descrs and class_label not in tutoring_user.classes:
                        unique_courses.append(course)
                        course_descrs.append(course['descr'])
                return render(request, 'home/courses.html', {'courses': unique_courses})
            
        elif request.method == 'POST': 
            # print("add is being clicked")
            selected_courses = request.POST.getlist('selected_courses')
            for course in selected_courses:
                tutoring_user.classes.append(course)
            tutoring_user.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render(request, 'home/courses.html', {'courses': []})   
    except Exception as e:
        print(e)
        raise e
    
class IndexView(generic.ListView):
    template_name = 'home/index.html'

class TutoringUserSignupView(SignupView):
    template_name = 'home/login.html'
    form_class = SignupForm
    view_name = 'tutoring_signup'

def tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form.clean()
            form.save(commit=True)
            return HttpResponseRedirect('/')
    else:
        form = TutorForm({'user': request.user})
        form.fields['user'].widget = HiddenInput()
    return render(request, 'home/tutorform.html', {'form':form})

def edit_profile(request):
    tutoring_user = request.user.tutoringuser
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        major = request.POST.get('major')
        pay_rate = request.POST.get('pay_rate')
        is_virtual = request.POST.get('is_virtual')
        new_location = request.POST.get('new_location') 
        locations_to_remove = request.POST.getlist('remove_location')
        classes_to_remove = request.POST.getlist('remove_classes')
        if 'is_virtual' in request.POST and request.POST['is_virtual'] == 'true':
            is_virtual = True
        else:
            is_virtual = False

        if new_location:
            tutoring_user.locations.append(new_location)

        if locations_to_remove:
            for location in locations_to_remove:
                tutoring_user.locations.remove(location)
        
        if classes_to_remove:
            for course in classes_to_remove:
                tutoring_user.classes.remove(course)

        # Update the TutoringUser object with the new values
        TutoringUser.objects.filter(pk=tutoring_user.pk).update(
            full_name=full_name,
            major=major,
            pay_rate=pay_rate,
            is_virtual=is_virtual,
            locations=tutoring_user.locations,
            classes=tutoring_user.classes
        )

        return HttpResponseRedirect('/profile/')
    else:
        classes = tutoring_user.classes
        new_classes = []
        for course in classes:
            course_parts = course.split()
            new_course = " ".join(course_parts[1:])
            new_classes.append(new_course)
        form_data = {
            'full_name': tutoring_user.full_name,
            'major': tutoring_user.major,
            'pay_rate': tutoring_user.pay_rate,
            'is_virtual': tutoring_user.is_virtual,
            'locations': tutoring_user.locations,
            'classes': classes,
        }
        form = TutorForm(initial=form_data)

    return render(request, 'home/editprofile.html', {'form': form, 'tutoring_user': tutoring_user, 'tutor_classes': new_classes})

def add_availability(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        # session_length = request.POST['session_length']
        

        tutor = TutoringUser.objects.get(user=request.user)

        # tutor.add_availability({'date': date,'time': time, 'session_length': session_length})
        tutor.add_availability({'date': date,'time': time})

        # Save the updated TutoringUser object
        tutor.save()
        # print(tutor)
        return redirect('/profile/') 
    else:
        tutor = TutoringUser.objects.get(user=request.user)
        available_slots = tutor.get_availability()
        # print(available_slots)
       
        return render(request, 'home/availability.html')  