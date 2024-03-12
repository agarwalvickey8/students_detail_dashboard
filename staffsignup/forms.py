from django import forms
from .models import NEETRegistration, StudentDetails

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class NEETRegistrationForm(forms.ModelForm):
    class Meta:
        model = NEETRegistration
        fields = ['NEETApplication', 'Mobile']
