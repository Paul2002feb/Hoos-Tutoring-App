from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from allauth.account.views import SignupView
from .forms import TutoringSignupForm

# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

class IndexView(generic.ListView):
    template_name = 'home/index.html'

class TutoringUserSignupView(SignupView):
    template_name = 'home/login.html'
    form_class = TutoringSignupForm
    view_name = 'tutoring_signup'