from django.urls import path
from . import views

urlpatterns = [
    path('payment_sucess', views.payment_sucess, name='payment_sucess'),#urlpatterns for homepage
    path('checkout/', views.check_out, name='checkout'),#urlpatterns for checkout
    path('billing_info/', views.billing_info, name='billing_info'),
]