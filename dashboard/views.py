from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import SignUpForm

class IndexView(TemplateView):
    template_name = "dashboard/index.html"

class signup_view(TemplateView):
    template_name='dashboard/signup.html'
    form_class=SignUpForm
    success_url= reverse_lazy('index')

    def form_valid(self,form):
        user= form.save()
        login(self.request,user)
        return super().form_valid(form)