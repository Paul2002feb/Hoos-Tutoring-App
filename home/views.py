from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
from .forms import TutoringSignupForm
from .forms import TutoringSocialSignupForm
import requests

# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def search_courses(request):
    return render(request, 'home/courses.html')

def result_query(request):
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&subject=CS&catalog_nbr=3240"
    response=requests.get(url).json()
    return render(request, 'requstcourses.html', {'response':response})

class IndexView(generic.ListView):
    template_name = 'home/index.html'

class TutoringUserSignupView(SignupView):
    template_name = 'home/login.html'
    form_class = TutoringSignupForm
    view_name = 'tutoring_signup'

class TutoringUserSocialSignupView(SocialSignupView):
    form_class = TutoringSocialSignupForm
    view_name = 'tutoring_social_signup'