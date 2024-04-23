from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput,TextInput

from .models import Record

# register a user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    
# login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)


# Creating a new record
class AddRecord(forms.ModelForm):

    class Meta:
        model = Record
        fields = ['first_name', 'last_name','email','phone','address','city','province','country']


# Updating a new record
class UpdateRecord(forms.ModelForm):

    class Meta:
        model = Record
        fields = ['first_name', 'last_name','email','phone','address','city','province','country']