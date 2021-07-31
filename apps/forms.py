from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')
    last_name = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'last_name')

class UserDelForm(forms.Form):
    name = forms.CharField()