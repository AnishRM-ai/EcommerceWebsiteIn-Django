from payment.models import Order, CancellationOrder

def order_notify(request):
    order = Order.objects.filter(status = 'Pending').count()
    return  {'notification_count': order}


def cancel_notify(request):
    cancel = CancellationOrder.objects.filter(mark_as_read = False).count()
    return {'cancel_count': cancel}
