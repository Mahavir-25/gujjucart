
from django.urls import path
from dashboard.views import IndexView,SignupView,ProfileView,LoginView,LogoutView,ForgotPasswordView,ResetPasswordView,ProfileUpdateView

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<int:user_id>/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ProfileUpdate/', ProfileUpdateView.as_view(), name='profileupdate'),

]
