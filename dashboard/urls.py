
from django.urls import path
from dashboard.views import IndexView,ToggleWishlistView,IndexLoginview,DashboardIndexView,SignupView,ProfileView ,ProductUpdateView,ProductDeleteView,ProductDetailView, ProductListView,AddProductView,LoginView,LogoutView,ForgotPasswordView,ResetPasswordView,ProfileUpdateView

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('admin-dashboard', DashboardIndexView.as_view(), name='dashboard_index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('index_login', IndexLoginview.as_view(), name='index_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<int:user_id>/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ProfileUpdate/', ProfileUpdateView.as_view(), name='profileupdate'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('toggle-wishlist/<int:product_id>/', ToggleWishlistView.as_view(), name='toggle_wishlist')     

]
