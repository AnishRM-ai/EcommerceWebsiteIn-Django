from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


        



#Customer Profile Creation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=15, blank=True)  # Phone number of the customer
    address1 = models.CharField(max_length=200, blank=True)# Address of the customer
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)   # Cart data stored here when a user is logged out.
    
    def __str__(self):
        return self.user.username + " profile"
    
#Create a user Profile by default when user sign ups
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
#Automate the profile saving
post_save.connect(create_profile, sender=User)    
    
    
        

#Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children' )
    category_image = models.ImageField(upload_to='uploads/category/')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
#Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    phone =  models.CharField(max_length=10)
    email =  models.EmailField(max_length=150)
    password =  models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

#all Products
class Product(models.Model):
    name =  models.CharField(max_length=100)
    price =  models.DecimalField(default=0, decimal_places=2, max_digits = 8)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description =  models.CharField(max_length=250, default='', blank = True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    
    
    # Add Sale Stuff
    is_sale = models.BooleanField(default= False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits = 8, null=True)
    
    #Add stock of the product
    in_stock =  models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name


         

#Customer Order Models
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    address = models.CharField(max_length=300, default='', blank = True)
    phone = models.CharField(max_length=20, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return {self.product}