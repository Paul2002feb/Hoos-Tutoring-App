from .models import TutoringUser
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from django.forms.widgets import HiddenInput
from django import forms
    
class TutorForm(forms.ModelForm):
    class Meta:
        model = TutoringUser
        fields = ('is_tutor','user','full_name','major', 'locations', 'is_virtual', 'pay_rate')
        
    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        self.fields['pay_rate'].required = False
        self.fields['locations'].required = False
    def clean(self):
        isTutor = self.cleaned_data.get('is_tutor')
        pay = self.cleaned_data.get('pay_rate')
        loc = self.cleaned_data.get('locations')
        if isTutor:
            msg = forms.ValidationError("This field is required.")
            if (pay is None):
                self.add_error('pay_rate', msg)
            if (loc is None):
                self.add_error('locations', msg)
        else:
            # Keep the database consistent. The user may have
            # submitted a shipping_destination even if shipping
            # was not selected
            self.cleaned_data['pay_rate'] = 0
            self.cleaned_data['locations'] = list()

        return self.cleaned_data
