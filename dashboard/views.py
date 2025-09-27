from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import SignUpForm,LoginForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.models import User


class LoginView(FormView):
    template_name = 'dashboard/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index') 

    def form_valid(self, form):
        user = form.get_user()  
        login(self.request, user) 
        return super().form_valid(form)

    def form_invalid(self, form):
       return super().form_invalid(form)
    

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/index.html"
    login_url = reverse_lazy('login')

class SignupView(FormView):
    template_name = 'dashboard/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':   # ✅ only bind on POST
            kwargs.update({'files': self.request.FILES})
        return kwargs
    def  form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response
        
class ForgotPasswordView(FormView):
    template_name = 'dashboard/forgot_password.html'
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        # Called when form passes validation
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        # Normally, send email with token; for now redirect to reset page
        return redirect('reset_password', user_id=user.id)

    def form_invalid(self, form):
        # Called when form fails validation
        return render(self.request, self.template_name, {'form': form}) 
    
     
class ResetPasswordView(FormView):
    template_name = 'dashboard/reset_password.html'
    form_class = ResetPasswordForm

    def dispatch(self, request, *args, **kwargs):
        # Get user_id from URL
        self.user_id = kwargs.get('user_id')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Called if form is valid
        password = form.cleaned_data['password1']
        user = User.objects.get(id=self.user_id)
        user.password = make_password(password)
        user.save()
        return redirect('login')  # Redirect after successful password reset

    def form_invalid(self, form):
        # Called if form has errors
        return render(self.request, self.template_name, {'form': form})