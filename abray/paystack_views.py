import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Cart, CartItem, Order, OrderItem, Course, Country, Profile
from django.utils.crypto import get_random_string
import uuid


@csrf_exempt
def place_order(request):
    import json
    data = json.loads(request.body)
    shipping_info = data.get('shippingInfo')
    email = shipping_info.get('email')
    name = shipping_info.get('name')
    cart = get_cart_from_request(request)

    if not cart or not cart.items.exists():
        return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)

    user_created = False
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        username = email
        password = get_random_string()
        first_name = name.split()[0]
        last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        country, _ = Country.objects.get_or_create(name=shipping_info.get('city', 'Unknown'))
        Profile.objects.create(user=user, country=country)
        user_created = True

    total_amount = sum(item.course.price * item.quantity for item in cart.items.all())

    order = Order.objects.create(
        user=user,
        full_name=name,
        email=email,
        address=shipping_info.get('address'),
        city=shipping_info.get('city'),
        zip_code=shipping_info.get('zip'),
        total_amount=total_amount,
        status='pending'
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            course=item.course,
            price=item.course.price,
            quantity=item.quantity
        )

    # Initiate Paystack payment
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    callback_url = request.build_absolute_uri('/verify-payment/')
    paystack_data = {
        'email': email,
        'amount': int(total_amount * 100),  # in kobo
        'currency': settings.PAYSTACK_CURRENCY,
        'callback_url': callback_url,
        'metadata': {
            'order_id': order.id
        }
    }
    response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=paystack_data)
    paystack_response = response.json()

    if paystack_response.get('status'):
        return JsonResponse({
            'success': True,
            'payment_url': paystack_response['data']['authorization_url'],
            'order_id': order.id,
            'user_created': user_created
        })
    else:
        return JsonResponse({'success': False, 'error': 'Failed to initiate payment'})


@csrf_exempt
def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
    response = requests.get(verify_url, headers=headers)
    result = response.json()

    if result.get('status') and result['data']['status'] == 'success':
        metadata = result['data']['metadata']
        order_id = metadata['order_id']
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.save()

        # Enroll user to purchased courses
        for item in order.items.all():
            item.course.students.add(order.user)

        return JsonResponse({'success': True, 'message': 'Payment verified and courses assigned.'})
    return JsonResponse({'success': False, 'error': 'Payment verification failed'})