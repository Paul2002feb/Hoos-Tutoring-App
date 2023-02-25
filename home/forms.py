from .models import TutoringUser
from allauth import SignupForm
from django import forms

class TutoringSignupForm(SignupForm):
    is_student = forms.BooleanField(default=False)
    is_tutor = forms.BooleanField(default=False)
    def save(self, request):
        user = super(TutoringSignupForm, self).save(request)
        tutoring_user = TutoringUser(
            is_student=self.is_student,
            company_name=self.is_tutor
        )
        tutoring_user.save()
        return tutoring_user
