from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'profile_image']
    def clean(self):
            cleaned_data = super().clean()
            first_name = cleaned_data.get('first_name')
            
            # Check if username already exists
            if User.objects.filter(username=first_name).exists():
                raise ValidationError("User with this username already exists. Please choose a different first name.")
            
            return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name']  # safe now, no duplicates
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile_image = self.cleaned_data.get('profile_image')
            UserProfile.objects.create(user=user, profile_image=profile_image)

        return user

class LoginForm(AuthenticationForm):
     username=forms.CharField(
          required=True,max_length=30,
          widget=forms.TextInput(attrs={'class': 'form-control'}))
     
     password=forms.CharField(
          required=True,
          label="password",
          widget=forms.PasswordInput(attrs={'class': 'form-control'}))
     
     error_messages = {
        'invalid_login': (
            "Enter a correct username and password."
        ),
        'inactive': ("This account is inactive."),
        }
     def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

