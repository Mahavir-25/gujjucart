
from django.urls import path
from dashboard.views import IndexView,SignupView
app_name = 'dashboard'
urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('signup', SignupView.as_view(), name='signup'),

]
