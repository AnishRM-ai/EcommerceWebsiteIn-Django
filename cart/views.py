from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {'cart_products': cart_products,   "quantities": quantities, "totals": totals,})




def cart_add(request):
    cart = Cart(request)
    
    # Check if the request is a POST request
    if request.method == 'POST' and request.POST.get('action') == 'POST':
        # Get data from POST request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
     

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)


        # Save to session
        cart.add(product=product, quantity=product_qty)
       
        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Your item has been added!")
        return response

    else:
        # Handle non-POST requests or invalid action
        return JsonResponse({'error': 'Invalid request'})
    
    
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        #call delete function
        cart.remove(product= product_id)
        
        response = JsonResponse({"product":product_id})
        messages.success(request, "Your item has been removed!")
        return response
       
        

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
      
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({"quantity":product_qty,})
        messages.success(request, "Your item has been updated!")
        return response
       
