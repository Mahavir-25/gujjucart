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
    template_name = 'dashboard/login.html'  # fallback, rarely used
    form_class = LoginForm
    home_index = 'dashboard/home_index.html'

    def get_success_url(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'u':
            return reverse_lazy('index')
        else:
            return reverse_lazy('dashboard_index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        # Pass all errors to home_index template
        error_list = []

        # Non-field errors (like invalid credentials)
        for err in form.non_field_errors():
            error_list.append(err)

        # Field-specific errors
        for field in form:
            for err in field.errors:
                error_list.append(f"{field.label}: {err}")

        return render(self.request, 'dashboard/home_index.html', {
        'login_form': form,
        'login_error': True,
        'login_error_list': error_list
        })

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard_index.html"
    
    
    login_url = '/login/' 
    redirect_field_name = 'next'  

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login first!")
        return super().dispatch(request, *args, **kwargs)

class IndexView(TemplateView):
    template_name = "dashboard/home_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fetch your products
        context['products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
        return context
    



class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/profile.html"
    login_url = reverse_lazy('login')

class SignupView(FormView):
    template_name = 'dashboard/signup.html'
    form_class = SignUpForm
    def get_success_url(self):
        user = self.request.user
        # Redirect based on role
        if getattr(user, 'role', None) == 'u':
            return reverse_lazy('index')  # replace with your index URL name
        else:
            return reverse_lazy('dashboard_index')

    def form_valid(self, form):
        # Save the user instance but don’t commit if using ModelForm
        user = form.save(commit=False)
        
        # Automatically assign role 'u'
        user.role = 'u'
        user.save()  # Save user to database
        
        # Authenticate and login
        raw_password = form.cleaned_data['password1']
        user = authenticate(self.request, username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
            
            # Redirect based on role (if needed)
            if getattr(user, 'role', None) == 'u':
                return redirect('index')
            else:
                return redirect('dashboard_index')
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