from django.contrib import admin
from django.urls import path
from e_shop import views as e_shop_views
from users import views as user_views
from warehouse import views as warehoue_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', e_shop_views.index, name='home'),
    path('index/', e_shop_views.index, name='index'),
    path('product/<int:id>/', e_shop_views.product, name='product-details'),
    path('support/', e_shop_views.support, name='support'),
    path('cart/<int:id>/', warehoue_views.add_to_cart, name='cart'),
    path('buy-now/<int:id>/', warehoue_views.buy_now, name='buy-now'),
    path('view-cart/', warehoue_views.view_cart, name='view-cart'),
    path('remove-from-cart/<int:id>/', warehoue_views.remove_item_from_cart, name='remove-from-cart'),
    path('orders/', warehoue_views.order, name='orders'),
    path('remove-orders/', warehoue_views.remove_from_orders, name='remove_orders'),
    # Auth
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('register/', user_views.user_registration, name='register'),
    path('verify/', user_views.verify_registration_code, name='verify'),
    path('resend-code/', user_views.resend_verification_code, name='resend-code'),
    # Password Reset URLs
    path('forgot-password/', user_views.forgot_password, name='forgot_password'),
    path('verify-reset-code/', user_views.verify_reset_code, name='verify_reset_code'),
    path('resend-reset-code/', user_views.resend_reset_code, name='resend_reset_code'),
    path('set-new-password/', user_views.set_new_password, name='set_new_password'),
    path('success/', e_shop_views.success, name='success'),
    path('seller/dashboard/', user_views.seller_dashboard, name='seller-dashboard'),
    # Seller product management
    path('seller/products/add/', e_shop_views.add_product, name='add-product'),
    path('seller/products/manage/', e_shop_views.manage_products, name='manage-products'),
    path('seller/products/edit/<int:product_id>/', e_shop_views.edit_product, name='edit-product'),
    path('seller/products/delete/<int:product_id>/', e_shop_views.delete_product, name='delete-product'),
    path('seller/settings/currency/', e_shop_views.currency_settings, name='currency-settings'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
