from django.urls import path, include

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='index'),
    path('login',views.TutoringUserSignupView.as_view(), name='login'),
    path('tutorform',views.tutor, name='tutorform'),
    path('requestlist', views.view_requests, name='requestlist'),
    path('tutorsearch', views.search_tutors, name='tutorsearch'),
    path('tutorprofile/<int:tutor_id>/', views.tutor_profile, name='tutor_profile'),
    path('favoritelist', views.view_favorites, name='favoritelist'),
    path('studentprofile/', views.student_profile_page, name='studentprofile'),
    path('studentprofile/edit_profile/', views.edit_student_profile, name='editstudentprofile'),
]