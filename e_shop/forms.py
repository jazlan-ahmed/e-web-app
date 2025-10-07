from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'color', 'originalPrice', 'offerPrice', 'currency',
            'availableOffers', 'highlights', 'description', 
            'image', 'company', 'category'
        ]
        widgets = {
            'availableOffers': forms.Textarea(attrs={'rows': 3}),
            'highlights': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'color': forms.TextInput(attrs={'placeholder': 'e.g., Red, Blue, Black'}),
            'originalPrice': forms.NumberInput(attrs={'placeholder': 'Original price'}),
            'offerPrice': forms.NumberInput(attrs={'placeholder': 'Offer price'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company/Brand name'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If editing existing product, populate seller field
        if self.instance and self.instance.pk and user:
            self.instance.seller = user.username
        
        # Set default currency based on user's preferred currency
        if user and hasattr(user, 'profile') and not self.instance.pk:
            self.fields['currency'].initial = user.profile.preferred_currency
        
        # Make category optional with better display
        self.fields['category'].required = False
        self.fields['category'].empty_label = "Select a category (optional)"

    def clean(self):
        cleaned_data = super().clean()
        original_price = cleaned_data.get('originalPrice')
        offer_price = cleaned_data.get('offerPrice')
        
        if original_price and offer_price and offer_price > original_price:
            raise forms.ValidationError("Offer price cannot be higher than original price.")
        
        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.seller = user.username
        if commit:
            instance.save()
        return instance


class SupportForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}))
