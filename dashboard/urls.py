
from django.urls import path
from dashboard.views import IndexView,signup_view

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('signup', signup_view.as_view(), name='signup'),

]
