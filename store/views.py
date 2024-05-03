from django.shortcuts import render, redirect
from .models import Product
from .models import Category, Profile, ClothingSize, Subcategory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoform
from django import forms
from django.db.models import Q
from django.contrib.auth.models import Group
from .forms import GroupUserLoginForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
import json
from cart.cart import Cart





#Seller Admin  Panel
def login_view(request):
    user = request.user
    is_seller_admin = user.groups.filter(name='Seller-Admin').exists()

    # If the user is already logged in, redirect to a specific page
    if request.user.is_authenticated:
        return redirect('home')
    
    # Handle POST request for login form submission
    if request.method == 'POST':
        form = GroupUserLoginForm(request, data=request.POST)
        if form.is_valid():
            # Get the authenticated user
            user = form.cleaned_data['user']
            # Log the user in
            login(request, user)
            
            # Redirect based on the user's group
            if user.groups.filter(name='Seller-Admin').exists():
                return redirect('dashboard')  # Redirect to a group-specific page
            else:
                return redirect('home')  # Redirect to the profile page
    else:
        form = GroupUserLoginForm()  # Create a new form for GET requests
    
    # Render the login form template
    return render(request, 'seller_login.html', {'form': form, 'is_seller_admin': is_seller_admin})
  


#search function
def search(request):
    """
    View function for handling search functionality
    if the request method is POST, it searches the product based on the provided search value and renders it to the search.html page. 
    if no products are found, a message is displayed informing the user.add()
    """
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
    """
    View function for Updating user details.
    
    if the user is authenticated, it gets current user id only if user exist.
    if user does not exist then error message is displayed.
    if the request method is POST then it checks if the form is valid, valid form is saved,
    non valid form is rejected and displays error message. 
    if the request is not POST then just a form is displayed.
    
    Returns -> Login page.
    """
    
    if request.user.is_authenticated:
        try:
            current_users = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            messages.error(request, "User profile does not exist.")
            return redirect('home')

        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)  # Create a new instance

        form = UserInfoform(request.POST or None, instance=current_users)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your Info Has been updated successfully")
                return redirect('home')
            else:
                messages.error(request, "Form is not valid.")
                return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
        else:
            return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})

    else:
        messages.error(request, "You need to be logged in to update your info.")
        return redirect('login')

#Update password
def update_password(request):
    """
    View function for updating password of the user.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
          HttpResponse: Redirects to the home page if the user is not authenticated.
                      Renders the 'update_password.html' template with the password change form if the user is authenticated.
                      Redirects to the 'update_user' page after successfully updating the password.
                      Redirects to the 'update_password' page if there are form validation errors.
    """
    # if requested user is authenticated
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
    """View function for updating user profile information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page if the user is not authenticated.
                      Renders the 'update_user.html' template with the user update form if the user is authenticated.
                      Redirects to the home page after successfully updating the user profile.
    """
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
    """
    View function for displaying a summary of categories and products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'category_summary.html' template with categories and products.
    """
    
    product = Product.objects.all()
    categories = Category.objects.filter()
    return render(request, 'category_summary.html', {"categories": categories, "product": product})

#function to display category of the products.
def category(request, foo):
    """
    View function for displaying products within a specific category.

    Args:
        request (HttpRequest): The HTTP request object.
        foo (str): The category name extracted from the URL.

    Returns:
        HttpResponse: Renders the 'category.html' template with products and the specified category.
                      Redirects to the home page if the category doesn't exist.
    """
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
    
   
#function to display details of the products.
def product(request, pk):
    """
    View function for displaying details about a product.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the product.

    Returns:
        HttpResponse: Renders the 'product.html' template with details about the specified product.
    """
    
    product = Product.objects.get(id = pk)
    sizes = ClothingSize.objects.all()
    return render(request, 'product.html', {'product': product, 'size':sizes})

#function to display home page.
def home(request):
    """
    View function for displaying the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template with all products.
    """
    
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

#function to display about page view
def about(request):
    """
    View function for displaying the about page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'about.html' template.
    """
    return render(request, 'about.html', {})

#function to handle login functionality
def login_user(request):
    """
    View function for handling user login.
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page after successful login.
                      Redirects back to the login page if login fails.
    """
    
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #Shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get users saved cart
            saved_cart = current_user.old_cart
            #Convert database string to python dict
            if saved_cart:
                #Convert to dict using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                #Loop through the cart and add the items from the database
                for key, value  in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                    
            messages.success(request, ("You have been logged in."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, loggin in! Try again!"))
            return redirect('login')   
          
    else:
        return render(request, 'login.html', {})

#function for logout 
def logout_user(request):
    """
    View function for handling user logout.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page after logout.
    """
    
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('home')

#function to register users
def register_user(request):
    """
    View function for handling user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'register.html' template with the registration form.
                      Redirects to the update user page after successful registration.
                      Redirects back to the registration page if registration fails.
    """
    
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