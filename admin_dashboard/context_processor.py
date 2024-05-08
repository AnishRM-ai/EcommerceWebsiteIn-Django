from payment.models import Order

def order_notify(request):
    order = Order.objects.filter(shipped = False).count()
    return  {'notification_count': order}

