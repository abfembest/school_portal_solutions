from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Course
from django.contrib.auth.models import User


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.save()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        cart = get_or_create_cart(request)

        item, created = CartItem.objects.get_or_create(cart=cart, course=course)
        if not created:
            item.quantity += 1
            item.save()
        return JsonResponse({'success': True})


@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        cart = get_or_create_cart(request)

        CartItem.objects.filter(cart=cart, course=course).delete()
        return JsonResponse({'success': True})


def get_cart(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('course')
    cart_data = [
        {
            'id': item.course.id,
            'title': item.course.title,
            'price': float(item.course.price),
            'quantity': item.quantity,
            'image': item.course.image.url if item.course.image else None,
        }
        for item in items
    ]
    return JsonResponse({'cartItems': cart_data})
