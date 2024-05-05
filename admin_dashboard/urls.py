from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dash, name='dashboard'),
    path('product_management/', views.productManage, name='productManagement'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('create_order/', views.create_order, name="create_order"),
    path('order_list', views.order_list, name="order_list"),
    path('order_list/<int:pk>/order_edit', views.order_edit, name="order_edit"),
    path('order_list/<int:pk>/order_delete', views.order_delete, name="order_delete"),
    
]
