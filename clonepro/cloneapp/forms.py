from django.forms import ModelForm
#from cloneapp.models import
from django.contrib.auth.models import User
from cloneapp.models import Videos
from django import forms

# Create the form class.
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
class SigninForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','password']
class Video_Upload_form(ModelForm):
    class Meta:
        model = Videos
        fields = ['title', 'description','videofile']
