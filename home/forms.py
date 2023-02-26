from .models import TutoringUser
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from django import forms

class TutoringSignupForm(SignupForm):
    is_tutor = forms.BooleanField()
    def signup(self, request, user):
        user.is_tutor = super(TutoringSignupForm, self).save(request)
        tutoring_user = TutoringUser(
            user=user,
            is_tutor=self.cleaned_data.get('is_tutor'),
        )
        tutoring_user.save()
        return tutoring_user.user

class TutoringSocialSignupForm(SocialSignup):
    is_tutor = forms.BooleanField()
    def save(self, request):
        user = super(TutoringSocialSignupForm, self).save(request)
        tutoring_user = TutoringUser(
            user = user,
            is_tutor=self.cleaned_data.get('is_tutor'),
        )
        tutoring_user.save()
        return tutoring_user.user
