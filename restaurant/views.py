from django.shortcuts import render
import random
import time

# accessed by multiple funcs so it's global 
daily_specials = [
        "The Brandon Surprise",
        "One Thousand Bees",
        "Lukewarm Diet Pepsi",
        "Onika Burger"
    ]


def main(request):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    context = {
        'current_time': current_time
    }
    return render(request, 'restaurant/main.html', context)

def order(request):
    daily_special = random.choice(daily_specials)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    context = {
        'daily_special': daily_special,
        'current_time': current_time
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        items_ordered = request.POST.getlist('items')
        extras_ordered = request.POST.getlist('extras')
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        special_instructions = request.POST.get('instructions')

        # Calculate total price using the new method
        total_price = calculate_total_price(items_ordered, extras_ordered)

        # Calculate ready time
        ready_time = time.localtime(time.time() + random.randint(30, 60) * 60)
        ready_time_str = time.strftime('%H:%M:%S', ready_time)

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        context = {
            'items_ordered': items_ordered,
            'extras_ordered': extras_ordered,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time_str,
            'current_time': current_time
        }
        return render(request, 'restaurant/confirmation.html', context)
    return render(request, 'restaurant/order.html')

def calculate_total_price(items_ordered, extras_ordered):
    prices = {
        "Pizza": 15,
        "Burger & Fries": 12,
        "Chicken Alfredo": 8,
        "Caesar Salad": 6,
        "Daily Special": 18.50
    }
    extras_prices = {
    "Extra Sauce Packets": 1.50,
    "Extra Utensils": 0.25,
    "Extra Cheese": 3,
    "Canned Soda": 2
    }
    total_price = 0
    for item in items_ordered:
        # Check if the item is in the daily specials list
        if item in daily_specials:
            total_price += prices["Daily Special"]
        else:
            total_price += prices.get(item, 0)
    
    for extra in extras_ordered:
        total_price += extras_prices.get(extra, 0)
    
    return f"{total_price:.2f}"