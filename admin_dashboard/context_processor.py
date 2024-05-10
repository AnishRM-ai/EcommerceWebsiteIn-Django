from payment.models import Order

def order_notify(request):
    order = Order.objects.filter(status = 'Pending').count()
    return  {'notification_count': order}

