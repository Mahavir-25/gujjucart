
from django.urls import path
from dashboard.views import IndexView,SignupView,LoginView,LogoutView,ForgotPasswordView,ResetPasswordView

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<int:user_id>/', ResetPasswordView.as_view(), name='reset_password'),

]
