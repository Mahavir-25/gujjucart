from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'id': 'id_first_name',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'id': 'id_last_name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'id': 'id_email',
            'class': 'form-control'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'id': 'id_username',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'id': 'id_password1',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'id': 'id_password2',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
