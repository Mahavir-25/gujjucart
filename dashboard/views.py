from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import SignUpForm,LoginForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin



class LoginView(FormView):
    template_name = 'dashboard/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')  # redirect after successful login

    def form_valid(self, form):
        # Called if form is valid
        user = form.get_user()  # get authenticated user from the form
        login(self.request, user)  # log the user in (session)
        return super().form_valid(form)

    def form_invalid(self, form):
        # Called if form is invalid
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
    def  form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response
        
    