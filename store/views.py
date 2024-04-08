from django.shortcuts import render, redirect
from .models import Product
from .models import Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoform
from django import forms
from django.db.models import Q

#search 
def search(request):
    #determine if they fill out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query the db models
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))  #icontains allows to search case insensitive .
        
        if not searched:
            messages.success(request, "Sorry, The Product you are searching for is not available!")
            return render(request, 'search.html', {"searched":searched})
        else:
            return render(request, 'search.html', {"searched":searched})
    else:
        return render(request, "search.html", {})

#Update user details
def update_info(request):
    if request.user.is_authenticated:
         try:
            current_users = Profile.objects.get(user__id=request.user.id)
         except Profile.DoesNotExist:
              # Handle the case where the user profile does not exist
            messages.error(request, "User profile does not exist.")
            return redirect('home')  # Redirect to home or appropriate page
        
         form = UserInfoform(request.POST or None, instance=current_users)
         if request.method == 'POST':   
          if form.is_valid():
            form.save()
            messages.success(request, "Your Info Has been updated successfully")
            return redirect('home')
          else:
                # Handle the case where form validation fails
                messages.error(request, "Form is not valid.")
                # You might want to render the form again to show validation errors.
                # Example: return render(request, 'update_info.html', {'form': form})
         else:
            # If it's not a POST request, just render the form
            return render(request, 'update_info.html', {'form': form})
    else:
        # Handle the case where the user is not authenticated
        messages.error(request, "You need to be logged in to update your info.")
        return redirect('login')  # Redirect to login page or appropriate page

#Update password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            #is the form valid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your Pass Has Been Updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
            
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form":form} )
    else:
        messages.error(request, "You Must be Logged In !!")
        return redirect('home')
        
        
        

#Update user details
def update_user(request):
    if request.user.is_authenticated:
        current_users = User.objects.get(id=request.user.id)
        user_form =UpdateUserForm(request.POST or None, instance=current_users)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_users)
            messages.success(request, "Profile updated successfully")
            return redirect('home')
        return render(request, "update_user.html", {"update_user": user_form} )
    else:
        messages.error(request, "You Must be Logged In !!")
        return redirect('home')
    



def category_summary(request):
    categories = Category.objects.filter()
    return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
    #Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        category = Category.objects.get(name=foo)
        
        #Look up the category
        if category.children.exists():
            child_categories = category.children.all()
            products = Product.objects.filter(category__in= child_categories)
        else:
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
            return redirect('update_user')
        else: 
            messages.success(request, ("Whoops! There was a problem in registering."))
            return redirect('register')
        
    return render(request, 'register.html', {'forms': form})