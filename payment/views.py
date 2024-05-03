from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
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


   