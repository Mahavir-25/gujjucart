from django.views.generic import TemplateView,CreateView,ListView,DetailView,DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView,UpdateView,FormView
from .forms import SignUpForm,LoginForm,ProductForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import ForgotPasswordForm, ResetPasswordForm,ProfileUpdateForm
from django.contrib.auth.models import User
from dashboard.models import Product


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



class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/profile.html"
    login_url = reverse_lazy('login')

class SignupView(FormView):
    template_name = 'dashboard/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        raw_password = form.cleaned_data['password1']
        user = authenticate(self.request, username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)  # ✅ Safe to call now
            return redirect('index')  # or your dashboard/homepage
        else:
            form.add_error(None, "Authentication failed. Please try logging in manually.")
            return self.form_invalid(form)
        
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
# profile update view

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'dashboard/update_profile.html'
    success_url = reverse_lazy('profile')  # redirect after successful update

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('product_list')  # redirect after successful add

    # Handle valid form
    def form_valid(self, form):
        messages.success(self.request, "✅ Product added successfully!")
        return super().form_valid(form)

    # Handle invalid form
    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Please correct the errors below.")
        return super().form_invalid(form)
    
class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/product_list.html'  # Your template
    context_object_name = 'products'
    paginate_by = 10 

    # Optional: show only active products
    def get_queryset(self):
        return Product.objects.filter().order_by('-created_at')
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'dashboard/product_view.html'  # your template path
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_form.html'  # same template as Add
    success_url = reverse_lazy('product_list')     # redirect after successful update

    # Handle valid form submission
    def form_valid(self, form):
        messages.success(self.request, "✅ Product updated successfully!")
        return super().form_valid(form)

    # Handle invalid form submission
    def form_invalid(self, form):
        messages.error(self.request, "⚠️ Please correct the errors below.")
        return super().form_invalid(form)
    
# ✅ Delete product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'dashboard/product_delete.html'
    success_url = reverse_lazy('product_list')