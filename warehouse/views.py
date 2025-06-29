from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Orders
from e_shop.models import Product
from users.models import Address
from users.form import UserAddress

def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    cart_item = Cart.objects.filter(name = product.name).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = Cart.objects.create(
            name = product.name,
            image = product.image,
            originalPrice = product.originalPrice,
            offerPrice = product.offerPrice,
            seller = product.seller,
            quantity = 1,
        )
    return render(request, 'go_to_cart.html')

def view_cart(request):
    cart_item = Cart.objects.all()
    quantity = 0
    price = 0
    discount = 0
    protection_fee = 0

    for item in cart_item:
        price += item.originalPrice*item.quantity
    for item in cart_item:
        discount += (item.originalPrice - item.offerPrice)*item.quantity
    for item in cart_item:
        protection_fee += 99*item.quantity
    for item in cart_item:
        quantity += item.quantity
    for item in cart_item:
        item.offer = round(((item.originalPrice - item.offerPrice)/item.originalPrice)*100)
        
    total_amount = (price+protection_fee)-discount
    savings = discount - protection_fee
    
    return render(request, 'cart.html', {'products' : cart_item,
            'count' : quantity,
            'price': price,
            'discount': discount,
            'protection_fee': protection_fee,
            'savings': savings,
            'tot_amount': total_amount,
            'count_gt_1': quantity > 1
    })

def remove_item_from_cart(request, id):
    item = get_object_or_404(Cart, pk=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return render(request, 'redirect_to_cart.html')

def order(request):
    items = Cart.objects.all()
    Orders.objects.all().delete()
    if not Orders.objects.all():
        for item in items:
            Orders.objects.get_or_create(
            name=item.name,
            image=item.image,
            originalPrice=item.originalPrice,
            offerPrice=item.offerPrice,
            seller=item.seller,
            quantity=item.quantity
            )

    orders = Orders.objects.all()

    quantity = 0
    price = 0
    discount = 0
    protection_fee = 0

    for item in orders:
        price += item.originalPrice*item.quantity
    for item in orders:
        discount += (item.originalPrice - item.offerPrice)*item.quantity
    for item in orders:
        protection_fee += 99*item.quantity
    for item in orders:
        quantity += item.quantity
    for item in orders:
        item.offer = round(((item.originalPrice - item.offerPrice)/item.originalPrice)*100)
        
    total_amount = (price+protection_fee)-discount
    savings = discount - protection_fee
    
    address = Address.objects.all()
    form = UserAddress()
    if request.method == 'POST':
        form = UserAddress(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Address.objects.get_or_create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                mobile = data['mobile'],
                pincode = data['pincode'],
                address = data['address'],
                city = data['city'],
                state = data['state'],
                landmark = data['landmark'],
                alternative_mobile = data['alternative_mobile']
            )
            return redirect('orders')
            
    return render(request, 'order_page.html', {'form' : form,
            'orders' : orders,
            'addresses' : address,
            'count' : quantity,
            'price': price,
            'discount': discount,
            'protection_fee': protection_fee,
            'savings': savings,
            'tot_amount': total_amount,
            'count_gt_1': quantity > 1
        })

def remove_from_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_item = get_object_or_404(Orders, pk=order_id)
        if order_item.quantity > 1:
            order_item.quantity -=1
            order_item.save()
        else:
            order_item.delete()

    orders = Orders.objects.all()

    quantity = 0
    price = 0
    discount = 0
    protection_fee = 0

    for item in orders:
        price += item.originalPrice*item.quantity
    for item in orders:
        discount += (item.originalPrice - item.offerPrice)*item.quantity
    for item in orders:
        protection_fee += 99*item.quantity
    for item in orders:
        quantity += item.quantity
    for item in orders:
        item.offer = round(((item.originalPrice - item.offerPrice)/item.originalPrice)*100)
        
    total_amount = (price+protection_fee)-discount
    savings = discount - protection_fee
    
    address = Address.objects.all()
    form = UserAddress()
    if request.method == 'POST':
        form = UserAddress(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Address.objects.get_or_create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                mobile = data['mobile'],
                pincode = data['pincode'],
                address = data['address'],
                city = data['city'],
                state = data['state'],
                landmark = data['landmark'],
                alternative_mobile = data['alternative_mobile']
            )
            return redirect('orders')
            
    return render(request, 'order_page.html', {'form' : form,
            'orders' : orders,
            'addresses' : address,
            'count' : quantity,
            'price': price,
            'discount': discount,
            'protection_fee': protection_fee,
            'savings': savings,
            'tot_amount': total_amount,
            'count_gt_1': quantity > 1
        })