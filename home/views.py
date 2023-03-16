from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from .forms import *
from django.forms.widgets import HiddenInput


# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

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