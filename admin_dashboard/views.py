from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from store.models import Product
from store.models import Category, ClothingSize
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.db.models import Q
from .forms import ProductForm
# Create your views here.
def admin_dash(request):
    return render(request, 'dashboard.html', {})

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
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'productadd.html', {'form': form})

# View to delete an existing product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})
