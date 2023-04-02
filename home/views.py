from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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


# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def notification_page(request):
    return render(request,'home/notificationpage.html')

def schedule_page(request):
    return render(request,'home/schedulepage.html')

def profile_page(request):
    return render(request,'home/profilepage.html')

def search_courses(request):
    if request.method == 'GET':
        input = request.GET.get('search-input')
        if input is None:
            return render(request, 'home/courses.html', {'courses': []})
        else:
            input_args = input.split()
            len_input = len(input_args)
            if len_input == 1:
                course_num = input_args[0]
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&class_nbr={course_num}'
                r = requests.get(url)
            elif len_input == 2:  # Use 'elif' instead of 'if' for multiple conditions
                department = input_args[0]
                mneomonic = input_args[1]
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject={department}&catalog_nbr={mneomonic}'
                r = requests.get(url)
            else:
                name = input.replace(" ","+")
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&keyword={input}'
                r = requests.get(url)
            courses = r.json()
            return render(request, 'home/courses.html', {'courses': courses})
    
    elif request.method == 'POST': 
        selected_courses = request.POST.getlist('selected_courses')
        user = request.user
        user.tutoring_user.classes.add(selected_courses)
        user.tutoring_user.save()
        return HttpResponseRedirect('/profile/')
    else:
        return render(request, 'home/courses.html', {'courses': []})

class IndexView(generic.ListView):
    template_name = 'home/index.html'

class TutoringUserSignupView(SignupView):
    template_name = 'home/login.html'
    form_class = SignupForm
    view_name = 'tutoring_signup'

class TutoringUserSocialSignupView(SocialSignupView):
    form_class = SocialSignup
    view_name = 'tutoring_social_signup'

def tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/')
    else:
        form = TutorForm({'user': request.user})
        form.fields['user'].widget = HiddenInput()
    return render(request, 'home/tutorform.html', {'form':form})

def edit_profile(request):
    tutoring_user = request.user.tutoringuser

    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutoring_user)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/profile/')
    else:
        form_data = {
            'full_name': tutoring_user.full_name,
            'major': tutoring_user.major,
            'pay_rate': tutoring_user.pay_rate,
            'locations': tutoring_user.locations,
            'is_virtual': 'true' if tutoring_user.is_virtual else 'false'
        }
        form = TutorForm(initial=form_data)
    return render(request, 'home/editprofile.html', {'form': form, 'tutoring_user': tutoring_user})

def update_requests(request):
    if request.method == 'POST':
        reqDict = dict(request.POST['event'])
        print(reqDict)
        tutorRequest = TutorRequest()
        tutorRequest.is_verified = False
        tutorRequest.request_user = request.user
        tutorRequest.request_tutor = request.POST['event']['title']
        tutorRequest.request_startTime = request.POST['event']['start']
        tutorRequest.request_endTime = (request.POST['event'])['end']
        tutorRequest.save()
        message = 'update successful'
    return HttpResponse(message)