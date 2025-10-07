from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Product, Category


@login_required(login_url='login')
def index(request):
    products = Product.objects.all()

    # Filtering by company (legacy) or category (new)
    companies_filter = request.GET.getlist('company')
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__name=category_filter)
    elif companies_filter:
        products = products.filter(company__in=companies_filter)

    for product in products:
        if product.originalPrice > 0:
            product.offer = round(((product.originalPrice - product.offerPrice) / product.originalPrice) * 100)

    # Categories from Category model; fallback to distinct companies if none defined
    categories_qs = Category.objects.order_by('name')
    if categories_qs.exists():
        categories = list(categories_qs.values_list('name', flat=True))
    else:
        categories = list(Product.objects.values_list('company', flat=True).distinct())

    # Top 3 popular products
    popular_products = Product.objects.order_by('-views')[:3]

    context = {
        'products': products,
        'companies': companies_filter,
        'categories': categories,
        'popular_products': popular_products,
        'active_category': category_filter,
    }
    return render(request, 'index.html', context)


def product(request, id):
    product = get_object_or_404(Product, pk=id)
    # increment popularity
    Product.objects.filter(pk=product.pk).update(views=F('views') + 1)
    # refresh value
    product.refresh_from_db()
    if product.originalPrice > 0:
        product.offer = round(((product.originalPrice - product.offerPrice) / product.originalPrice) * 100)
    return render(request, 'product.html', {'product': product})


from .forms import SupportForm
from .models import SupportRequest
from django.core.mail import send_mail
from django.conf import settings

def support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sr = SupportRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message'],
            )
            # Email to support inbox if configured
            support_to = getattr(settings, 'SUPPORT_INBOX_EMAIL', None)
            if support_to:
                try:
                    send_mail(
                        subject=f"Support: {sr.subject}",
                        message=f"From: {sr.name} <{sr.email}>\n\n{sr.message}",
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                        recipient_list=[support_to],
                        fail_silently=not settings.DEBUG,
                    )
                except Exception:
                    pass
            messages.success(request, 'Thanks! Your message has been sent.')
            return render(request, 'contact.html', {'form': SupportForm()})
    else:
        form = SupportForm()
    return render(request, 'contact.html', {'form': form})


def success(request):
    return render(request, 'success.html')


# Seller product management views
@login_required(login_url='login')
def add_product(request):
    from .forms import ProductForm
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.account_type != 'seller':
        messages.error(request, 'Only sellers can add products.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(user=request.user)
            messages.success(request, f'Product "{product.name}" has been added successfully!')
            return redirect('manage-products')
    else:
        form = ProductForm(user=request.user)
    
    return render(request, 'add_product.html', {'form': form})


@login_required(login_url='login')
def manage_products(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.account_type != 'seller':
        messages.error(request, 'Only sellers can manage products.')
        return redirect('home')
    
    # Get products for this seller
    products = Product.objects.filter(seller=request.user.username).order_by('-id')
    
    return render(request, 'manage_products.html', {'products': products})


@login_required(login_url='login')
def edit_product(request, product_id):
    from .forms import ProductForm
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.account_type != 'seller':
        messages.error(request, 'Only sellers can edit products.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user.username)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            product = form.save(user=request.user)
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('manage-products')
    else:
        form = ProductForm(instance=product, user=request.user)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required(login_url='login')
def delete_product(request, product_id):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.account_type != 'seller':
        messages.error(request, 'Only sellers can delete products.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user.username)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('manage-products')
    
    return render(request, 'delete_product_confirm.html', {'product': product})


@login_required(login_url='login')
def currency_settings(request):
    from users.forms import ProfileUpdateForm
    profile = getattr(request.user, 'profile', None)
    if not profile:
        messages.error(request, 'User profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Currency preference updated successfully!')
            # Redirect based on account type
            if profile.account_type == 'seller':
                return redirect('seller-dashboard')
            else:
                return redirect('home')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'currency_settings.html', {'form': form})
