from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'in_stock', 'image', 'is_sale', 'sale_price']