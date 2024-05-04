from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress
from django.contrib import messages


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
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


   