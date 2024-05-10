from store.models import Product
import datetime
from store.models import Profile
from decimal import Decimal

class Cart():
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        
        #if the user is new, no session key, Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available on all pages of sites
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        # Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Converting single quotation to double for Json
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to user profile model
            current_user.update(old_cart=str(carty))
      
    def add(self, product,quantity):
      
        product_id = str(product.id)
        product_qty = str(quantity)
        
        # Logic
        if product_id in self.cart:
            pass
        else:
           
             self.cart[product_id] = product_qty
          

        self.session.modified = True
        
        # Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Converting single quotation to double for Json
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to user profile model
            current_user.update(old_cart=str(carty))
      
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        #Return those lookup products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
    
        # get cart
        ourcart = self.cart
        #update dictionary/cart
        ourcart[product_id] = product_qty 
        
        self.session.modified = True
        thing = self.cart
        
         # Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Converting single quotation to double for Json
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to user profile model
            current_user.update(old_cart=str(carty))
        return thing
    
    def remove(self, product):
        product_id = str(product)
        #delete from dict/cart
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
         # Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Converting single quotation to double for Json
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to user profile model
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
         #get prod id
        product_id= self.cart.keys()
        #lookup those keys in our products db models
        products = Product.objects.filter(id__in=product_id)
        #get quantities
        quantities = self.cart
        total = Decimal('0') #initializing at 0
        for key, value in quantities.items():
            key = int(key)#convert into int from str
            for product in products:
                if product.id == key:
                  
                    if product.is_sale:
                        total = (total + product.sale_price * Decimal(value))
                    else:
                        total = (total + product.price * Decimal(value))
        
        
        return total
    
  
        
                    