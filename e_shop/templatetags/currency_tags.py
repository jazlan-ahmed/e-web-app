# e_shop/templatetags/currency_tags.py
from django import template
from ..currency_service import CurrencyConverter

register = template.Library()

@register.filter
def convert_currency(amount, currencies):
    """
    Convert amount from one currency to another
    Usage: {{ amount|convert_currency:"USD,EUR" }}
    """
    if not currencies:
        return amount
        
    try:
        from_currency, to_currency = currencies.split(',')
        return CurrencyConverter.convert_price(float(amount), from_currency.strip(), to_currency.strip())
    except:
        return amount

@register.filter
def currency_symbol(currency_code):
    """
    Get currency symbol for a currency code
    Usage: {{ "USD"|currency_symbol }}
    """
    return CurrencyConverter.get_currency_symbol(currency_code)

@register.simple_tag
def convert_product_price(product, user):
    """
    Convert product price to user's preferred currency
    Usage: {% convert_product_price product user %}
    """
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return {
            'original_price': product.originalPrice,
            'offer_price': product.offerPrice,
            'currency_symbol': product.get_currency_symbol(),
            'currency_code': product.currency,
        }
    
    user_currency = user.profile.preferred_currency
    product_currency = product.currency
    
    if user_currency == product_currency:
        return {
            'original_price': product.originalPrice,
            'offer_price': product.offerPrice,
            'currency_symbol': product.get_currency_symbol(),
            'currency_code': product.currency,
        }
    
    # Convert prices
    converted_original = CurrencyConverter.convert_price(
        product.originalPrice, product_currency, user_currency
    )
    converted_offer = CurrencyConverter.convert_price(
        product.offerPrice, product_currency, user_currency
    )
    
    return {
        'original_price': converted_original,
        'offer_price': converted_offer,
        'currency_symbol': CurrencyConverter.get_currency_symbol(user_currency),
        'currency_code': user_currency,
        'is_converted': True,
        'original_currency': product_currency,
    }

@register.inclusion_tag('currency_price.html')
def show_product_price(product, user):
    """
    Inclusion template tag to show product price with conversion
    Usage: {% show_product_price product user %}
    """
    price_info = convert_product_price(product, user)
    return {
        'product': product,
        'price_info': price_info,
        'user': user,
    }