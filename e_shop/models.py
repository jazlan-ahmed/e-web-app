from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SupportRequest(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Product(models.Model):
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
    
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    originalPrice = models.IntegerField()
    offerPrice = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    availableOffers = models.TextField()
    highlights = models.TextField()
    seller = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    company = models.TextField(max_length=50)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    # popularity tracking
    views = models.PositiveIntegerField(default=0)
    
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
        return currency_symbols.get(self.currency, '₹')
