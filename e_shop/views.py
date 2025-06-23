from django.shortcuts import render, get_object_or_404
from .models import Product, Cart
from django.shortcuts import render
from .form import ContactForm

# Create your views here.

def index(request):
    products = Product.objects.all()
    for product in products:
        if product.originalPrice > 0:
            product.offer = round(((product.originalPrice - product.offerPrice) / product.originalPrice) * 100)
    companies = request.GET.getlist('company')
    if companies:
        return render(request, 'index.html', {'companies' : companies, 'products' : products})
    return render(request, 'index.html', {'products' : products})

def product(request, id):
    product = get_object_or_404(Product,pk = id)
    if product.originalPrice > 0:
        product.offer = round(((product.originalPrice - product.offerPrice) / product.originalPrice) * 100)
    return render(request, 'product.html',{'product' : product})

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
