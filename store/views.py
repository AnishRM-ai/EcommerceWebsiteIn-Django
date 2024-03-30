from django.shortcuts import render, redirect
from .models import Product
from .models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def category(request, foo):
    #Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        #Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'products': products, 'category': category})
        
    except:
        messages.success(request, ("The Category Doesnt exist."))
        return redirect('home')
    
   

def product(request, pk):
    product = Product.objects.get(id = pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, loggin in! Try again!"))
            return redirect('login')
            
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('Account created successfully'))
            return redirect('home')
        else: 
            messages.success(request, ("Whoops! There was a problem in registering."))
            return redirect('register')
        
    return render(request, 'register.html', {'forms': form})