from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput,TextInput


# register a user
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    
# login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)
