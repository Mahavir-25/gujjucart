from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import SignUpForm
from django.views.generic.edit import FormView
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = "dashboard/index.html"
class LoginView(TemplateView):
    template_name="dashboard/login.html"
class SignupView(FormView):
    template_name = 'dashboard/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
    def  form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response
        
    