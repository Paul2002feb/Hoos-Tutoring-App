from .models import TutoringUser
from allauth.account.forms import SignupForm
from django import forms

class TutoringSignupForm(SignupForm):
    is_tutor = forms.BooleanField()
    def save(self, request):
        user = super(TutoringSignupForm, self).save(request)
        tutoring_user = TutoringUser(
            is_tutor=self.is_tutor,
        )
        tutoring_user.save()
        return tutoring_user
