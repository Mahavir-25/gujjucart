
from django.urls import path
from dashboard.views import IndexView,DeleteCartItemView,CartPageView,UpdateCartQuantityView,GetCartCountView,AddToCartView,UserProductDetailView,GetWishlistView,UserProfileView,ToggleWishlistView,IndexLoginview,IndexSignupView,DashboardIndexView,SignupView,ProfileView ,ProductUpdateView,ProductDeleteView,ProductDetailView, ProductListView,AddProductView,LoginView,LogoutView,ForgotPasswordView,ResetPasswordView,ProfileUpdateView

urlpatterns = [
   
    path('', IndexView.as_view(), name='index'),
    path('admin-dashboard', DashboardIndexView.as_view(), name='dashboard_index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('index_login', IndexLoginview.as_view(), name='index_login'),
    path('index_signup', IndexSignupView.as_view(), name='index_signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<int:user_id>/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_profile/',UserProfileView.as_view(), name='user_profile'),
    path('ProfileUpdate/', ProfileUpdateView.as_view(), name='profileupdate'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('toggle-wishlist/<int:product_id>/', ToggleWishlistView.as_view(), name='toggle_wishlist'),  
    path('get-wishlist/', GetWishlistView.as_view(), name='get_wishlist'),
    path('get-cart-count/', GetCartCountView.as_view(), name='get_cart_count'),    path('product/<slug:slug>/', UserProductDetailView.as_view(), name='user_product_detail'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartPageView.as_view(), name='cart_page'),
    path('update-cart-quantity/', UpdateCartQuantityView.as_view(), name='update_cart_quantity'),
    path('delete-cart-item/', DeleteCartItemView.as_view(), name='delete_cart_item'),

]
