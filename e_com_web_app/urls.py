from django.contrib import admin
from django.urls import path
from e_shop import views as e_shop_views
from users import views as user_views
from warehouse import views as warehoue_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('index/', e_shop_views.index, name='index'),
    path('product/<int:id>/', e_shop_views.product, name='product-details'),
    path('cart/<int:id>/', warehoue_views.add_to_cart, name='cart'),
    path('view-cart/', warehoue_views.view_cart, name='view-cart'),
    path('remove-from-cart/<int:id>/', warehoue_views.remove_item_from_cart, name='remove-from-cart'),
    path('orders/', warehoue_views.order, name='orders'),
    path('remove-orders/', warehoue_views.remove_from_orders, name='remove_orders'),
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.user_registeration, name='register'),
    path('success/', e_shop_views.success, name='success')
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)