from django.shortcuts import render
from .models import *
from listings.models import *
from django.http import JsonResponse
import json
# Create your views here.
from listings.models import Product
import datetime


def cart(request):

    if(request.user.is_authenticated):
        current_user = request.user
        order, created = Order.objects.get_or_create(user=current_user, complete=False)
        #geting all order items that have that current item as parent
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context ={
        'items':items,
        'order':order,
    }
    return render(request, 'orders/cart.html',context)

def checkout(request):
    if(request.user.is_authenticated):
        current_user = request.user
        order, created = Order.objects.get_or_create(user=current_user, complete=False)
        #geting all order items that have that current item as parent
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context ={
        'items':items,
        'order':order,
    }
    return render(request, 'orders/checkout.html',context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    current_user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=current_user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if(action == 'add'):
        orderItem.quantity = (orderItem.quantity+1)
    elif(action=='remove'):
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if(orderItem.quantity<=0):
        orderItem.delete()

    print(f'Action: {action}, productId: {productId}')
    return JsonResponse('Item was added',safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if(request.user.is_authenticated):
        current_user = request.user
        order, created = Order.objects.get_or_create(user=current_user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if(total==order.get_cart_total):
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            user = current_user,
            order = order,
            address = data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    else:
        print('User is nor logged in')
    return JsonResponse('Payment complete!',safe=False)