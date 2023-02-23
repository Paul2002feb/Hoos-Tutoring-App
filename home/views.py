from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question
from django.views import generic

# Create your views here.
def home(request):
    return HttpResponse("Hello, world.")

class IndexView(generic.ListView):
    template_name = 'home/index.html'