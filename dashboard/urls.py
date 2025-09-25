
from django.urls import path
from dashboard.views import IndexView,SignupView,LoginView

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('LoginView', LoginView.as_view(), name='login'),

]
