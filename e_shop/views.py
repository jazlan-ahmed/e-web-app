from django.shortcuts import render, get_object_or_404
from .models import Product

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

def success(request):
    return render(request, 'success.html')
