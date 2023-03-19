from django.urls import path, include

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='index'),
    path('login',views.TutoringUserSignupView.as_view(), name='login'),
    path('socialsignup',views.TutoringUserSocialSignupView.as_view(), name='socialsignup'),
    path('accounts/', include('allauth.urls')),
    path('tutorform',views.tutor, name='tutorform')
]