from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='This field is required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class OrderFrom(forms.Form):
    city = forms.CharField()
    street = forms.CharField()
    building = forms.CharField()
    flat = forms.IntegerField()
    phone = forms.IntegerField()
