from payment.models import Order


#user order notification
def user_order_notify(request):
    user = request.user.pk
    order = Order.objects.filter(user = user, status = 'Pending').count()
    return  {'user_order_count': order}