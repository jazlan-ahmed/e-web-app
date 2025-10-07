# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50, default="India")
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    alternative_mobile = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.state}, {self.country}"


# ✅ New Profile model
class Profile(models.Model):
    ACCOUNT_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('INR', 'Indian Rupee (₹)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
        ('CNY', 'Chinese Yuan (¥)'),
        ('CHF', 'Swiss Franc (CHF)'),
        ('KRW', 'South Korean Won (₩)'),
        ('SGD', 'Singapore Dollar (S$)'),
        ('HKD', 'Hong Kong Dollar (HK$)'),
        ('NZD', 'New Zealand Dollar (NZ$)'),
        ('SEK', 'Swedish Krona (kr)'),
        ('NOK', 'Norwegian Krone (kr)'),
        ('DKK', 'Danish Krone (kr)'),
        ('PLN', 'Polish Złoty (zł)'),
        ('CZK', 'Czech Koruna (Kč)'),
        ('HUF', 'Hungarian Forint (Ft)'),
        ('RUB', 'Russian Ruble (₽)'),
        ('BRL', 'Brazilian Real (R$)'),
        ('MXN', 'Mexican Peso ($)'),
        ('AED', 'UAE Dirham (د.إ)'),
        ('SAR', 'Saudi Riyal (﷼)'),
        ('THB', 'Thai Baht (฿)'),
        ('MYR', 'Malaysian Ringgit (RM)'),
        ('PHP', 'Philippine Peso (₱)'),
        ('IDR', 'Indonesian Rupiah (Rp)'),
        ('VND', 'Vietnamese Dong (₫)'),
        ('TWD', 'Taiwan Dollar (NT$)'),
        ('TRY', 'Turkish Lira (₺)'),
        ('ZAR', 'South African Rand (R)'),
        ('EGP', 'Egyptian Pound (£)'),
        ('NGN', 'Nigerian Naira (₦)'),
        ('KES', 'Kenyan Shilling (KSh)'),
        ('MAD', 'Moroccan Dirham (MAD)'),
        ('JOD', 'Jordanian Dinar (JD)'),
        ('KWD', 'Kuwaiti Dinar (KD)'),
        ('BHD', 'Bahraini Dinar (BD)'),
        ('OMR', 'Omani Rial (OMR)'),
        ('QAR', 'Qatari Riyal (QR)'),
        ('PKR', 'Pakistani Rupee (Rs)'),
        ('BDT', 'Bangladeshi Taka (৳)'),
        ('LKR', 'Sri Lankan Rupee (Rs)'),
        ('NPR', 'Nepalese Rupee (Rs)'),
        ('MMK', 'Myanmar Kyat (K)'),
        ('KHR', 'Cambodian Riel (៛)'),
        ('LAK', 'Lao Kip (₭)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES, default='buyer')
    preferred_currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='INR',
        help_text='Your preferred currency for viewing prices'
    )

    def get_currency_symbol(self):
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
        return currency_symbols.get(self.preferred_currency, '₹')
    
    def __str__(self):
        return f"{self.user.username} - {self.account_type}"
