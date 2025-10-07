# e_shop/currency_service.py
import requests
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CurrencyConverter:
    """
    Currency conversion service using free exchange rate API
    """
    
    # Free API endpoint (no API key required)
    BASE_URL = "https://api.exchangerate-api.com/v4/latest/"
    CACHE_TIMEOUT = 3600  # Cache rates for 1 hour
    
    @staticmethod
    def get_exchange_rate(from_currency, to_currency):
        """
        Get exchange rate from one currency to another
        Returns 1.0 if conversion fails or currencies are the same
        """
        if from_currency == to_currency:
            return 1.0
            
        cache_key = f"exchange_rate_{from_currency}_{to_currency}"
        
        # Try to get from cache first
        rate = cache.get(cache_key)
        if rate is not None:
            return rate
            
        try:
            # Fetch exchange rates from API
            response = requests.get(f"{CurrencyConverter.BASE_URL}{from_currency}", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            if to_currency in rates:
                rate = rates[to_currency]
                # Cache the rate
                cache.set(cache_key, rate, CurrencyConverter.CACHE_TIMEOUT)
                return rate
            else:
                logger.warning(f"Currency {to_currency} not found in exchange rates")
                return 1.0
                
        except Exception as e:
            logger.error(f"Error fetching exchange rate from {from_currency} to {to_currency}: {e}")
            return 1.0
    
    @staticmethod
    def convert_price(amount, from_currency, to_currency):
        """
        Convert price from one currency to another
        Returns the original amount if conversion fails
        """
        if from_currency == to_currency:
            return amount
            
        rate = CurrencyConverter.get_exchange_rate(from_currency, to_currency)
        return round(amount * rate, 2)
    
    @staticmethod
    def get_currency_symbol(currency_code):
        """
        Get currency symbol for a currency code
        """
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'INR': '₹',
            'JPY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CNY': '¥',
            'CHF': 'CHF',
            'KRW': '₩',
            'SGD': 'S$',
            'HKD': 'HK$',
            'NZD': 'NZ$',
            'SEK': 'kr',
            'NOK': 'kr',
            'DKK': 'kr',
            'PLN': 'zł',
            'CZK': 'Kč',
            'HUF': 'Ft',
            'RUB': '₽',
            'BRL': 'R$',
            'MXN': '$',
            'AED': 'د.إ',
            'SAR': '﷼',
            'THB': '฿',
            'MYR': 'RM',
            'PHP': '₱',
            'IDR': 'Rp',
            'VND': '₫',
            'TWD': 'NT$',
            'TRY': '₺',
            'ZAR': 'R',
            'EGP': '£',
            'NGN': '₦',
            'KES': 'KSh',
            'MAD': 'MAD',
            'JOD': 'JD',
            'KWD': 'KD',
            'BHD': 'BD',
            'OMR': 'OMR',
            'QAR': 'QR',
            'PKR': 'Rs',
            'BDT': '৳',
            'LKR': 'Rs',
            'NPR': 'Rs',
            'MMK': 'K',
            'KHR': '៛',
            'LAK': '₭',
        }
        return currency_symbols.get(currency_code, currency_code)