from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User


#Process the customer order
def process_order(request):
    if request.POST:
       cart = Cart(request)
       cart_products = cart.get_prods
       quantities = cart.get_quants
       totals = cart.cart_total()
        # Get Billing info from the user
       payment_form = PaymentForm(request.POST or None)
       
       my_shipping = request.session.get('my_shipping')
       
       # Gather Order Info
       fullname=my_shipping['shipping_fullname']
       email=my_shipping['shipping_email']
       # Create shipping address from session info
       shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']} \n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']} \n {my_shipping['shipping_country']}"
       amount_paid = totals
       
       if request.user.is_authenticated:
           #logged in user
           user = request.user
           #Create order
           create_order = Order(user=user, fullname = fullname, email=email, shipping_address=shipping_address, amount_paid=totals)
           create_order.save()
           messages.success(request, "Ordered Placed!")
           return redirect('home')
       else:
           #logged out user/no user account
           create_order = Order(fullname = fullname, email=email, shipping_address=shipping_address, amount_paid=totals)
           create_order.save()
           messages.success(request, "Ordered Placed!")
           return redirect('home')
       
       
       
       messages.success(request, "Ordered Placed!")
       return redirect('home')
       
       
        
    else:
        messages.success(request, "Access Denied, You must be logged in to view this page!")
        return redirect('home')





#Function to get billing info of the customer.
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        #GET shipping info session
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
   # checking if the user is logged in
        if request.user.is_authenticated:
           #Get Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals":totals, "shipping_info": request.POST, "billing_form":billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals":totals, "shipping_info": request.POST, "billing_form":billing_form})
    else:
        messages.success(request, "Access Denied, You must be logged in to view this page!")
        return redirect('home')


# Create your views here.
def payment_sucess(request):
    return render(request, 'payment/payment_sucess.html', {})

#Checkout Page
def check_out(request):
    # Get Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        #Checkout as user
        #Shipping User
        shipping_user = ShippingAddress.objects.get(user=request.user)
        #Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {'cart_products': cart_products,   "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        #Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {'cart_products': cart_products,   "quantities": quantities, "totals": totals,"shipping_form": shipping_form })


   