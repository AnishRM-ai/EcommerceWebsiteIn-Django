from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #urlpatterns for homepage
    path('about/', views.about, name='about'),#urlpatterns for about page
    path('login/', views.login_user, name='login'),#urlpatterns for login page for user/customer
    path('seller_login/', views.login_view, name='seller_login'),#urlpatterns for seller admin login page
    path('logout/', views.logout_user, name='logout'),#urlpatterns for logout page
    path('register/', views.register_user, name='register'),#urlpatterns for register page
    path('product/<int:pk>', views.product, name='product'),#urlpatterns for product page
    path('category/<str:foo>', views.category, name='category'),#urlpatterns for category page
    path('category_summary/', views.category_summary, name='category_summary'),#urlpatterns for category summary page
    path('updateUser/', views.update_user, name="update_user"),#urlpatterns for updating user info page
    path('update_info/', views.update_info, name="update_info"),#urlpatterns for update info page
    path('update_password/', views.update_password, name='update_password'),#urlpatterns for updating password page
    path('search/', views.search, name='search'),#urlpatterns for search bar
     path('checkout/', views.check_out, name='checkout'),#urlpatterns for chgeckout
]
