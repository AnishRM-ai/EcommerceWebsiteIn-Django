from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, CancellationOrder

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "fullname","email", "shipping_address", "amount_paid", "date_ordered" , "status", "shipped_date"]
    inlines = [OrderItemInline]
    
admin.site.register(CancellationOrder)   
# unregister order model
admin.site.unregister(Order)

# Re-Register our Order And OrderItems
admin.site.register(Order, OrderAdmin)