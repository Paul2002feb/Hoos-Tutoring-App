from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
import requests
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from .forms import *
from django.forms.widgets import HiddenInput


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
            if len_input is 1:
                course_num = input_args[0]
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&class_nbr={course_num}'
                r = requests.get(url)
            if len_input is 2:
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
    else:
        return render(request, 'home/courses.html', {'courses': []})

# def result_query(request):
#     return render(request, 'requstcourses.html')

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