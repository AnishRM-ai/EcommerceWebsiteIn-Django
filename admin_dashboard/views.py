from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from store.models import Product
from store.models import Category, ClothingSize
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.db.models import Q
from .forms import ProductForm, OrderForm, OrderItemForm, OrderItemFormSet
from payment.models import Order, OrderItem
from django.contrib.auth.models import User

#Function to create Order
def create_order(request):
    form = OrderForm(request.POST, request.FILES)
    return render(request, 'order_create.html', {'form': form})
           
# Order List       
def order_list(request):
    orderList = Order.objects.all()
    return render(request, 'order_list.html', {'order_list': orderList})

#Editing orders .
def order_edit(request, pk):
    order = get_object_or_404(Order, id=pk)
    form = OrderForm(instance=order)
    order_item_formset = OrderItemFormSet(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        order_item_formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and order_item_formset.is_valid:
            form.save()
            order_item_formset.save()
            messages.success(request, "Order successfully updated!")
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'orderform': form, 'order_item_formset': order_item_formset, 'order': order})

#Delete orders.
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'order_delete.html', {'order_del': order})


# Create your views here.
def admin_dash(request):
    product = Product.objects.count()
    orders = Order.objects.count()
    order_pending = Order.objects.filter(shipped = False).count()
    users = User.objects.count()
    return render(request, 'dashboard.html', {'count': product, 'order_count': orders, 'pending_order': order_pending, 'user':users})

def productManage(request):
    return render(request, 'productadd.html', {})


# View to list all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# View to create a new product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully Added!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'productadd.html', {'form': form})

# View to update an existing product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully Updated!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'productadd.html', {'form': form})

# View to delete an existing product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product successfully removed!")
        return redirect('product_list')
    return render(request, 'product_delete.html', {'product': product})
