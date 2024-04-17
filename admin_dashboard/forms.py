from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
   # Custom form fields with Bootstrap classes and specific placeholder texts
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
        required=True
    )
    category = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Category'}),
        required=True
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description', 'rows': 4}),
        required=True
    )
    price = forms.DecimalField(
        label="",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        required=True
    )
    in_stock = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
        required=True
    )
    image = forms.ImageField(
        label="",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True
    )
    is_sale = forms.BooleanField(
        label="Is Sale`",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    sale_price = forms.DecimalField(
        label="",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sale Price'}),
        required=False
    )
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'in_stock', 'image', 'is_sale', 'sale_price']
        