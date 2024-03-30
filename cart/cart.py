from store.models import Product
import datetime

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        
        #if the user is new, no session key, Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available on all pages of sites
        self.cart = cart
        
    def add(self, product,quantity):
      
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
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
        return thing
    
    def remove(self, product):
        product_id = str(product)
        #delete from dict/cart
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        
    def cart_total(self):
        #get prod id
        product_id= self.cart.keys()
        #lookup those keys in our products db models
        products = Product.objects.filter(id__in=product_id)
        #get quantities
        quatities = self.cart
        total = 0 #initializing at 0
        for key, value in quatities.items():
            key = int(key)#convert into int from str
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = (total + product.sale_price * value)
                    else:
                        total = (total + product.price * value)
        
        
        return total
                    