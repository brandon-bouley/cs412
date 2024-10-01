from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_specials = [
        "The Brandon Surprise",
        "One Thousand Bees",
        "Lukewarm Diet Pepsi",
        "Onika Burger"
    ]
    daily_special = random.choice(daily_specials)
    context = {
        'daily_special': daily_special
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        items_ordered = request.POST.getlist('items')
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        special_instructions = request.POST.get('instructions')

        # Calculate total price (assuming each item is $10 for simplicity)
        total_price = len(items_ordered) * 10

        # Calculate ready time
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        context = {
            'items_ordered': items_ordered,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%H:%M:%S')
        }
        return render(request, 'restaurant/confirmation.html', context)
    return render(request, 'restaurant/order.html')