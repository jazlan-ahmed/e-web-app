# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Countries, States, and Cities Data
location_data = {
    "India": {
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Delhi": ["New Delhi", "Dwarka", "Saket"],
        "Karnataka": ["Bangalore", "Mysore"],
    },
    "Pakistan": {
        "Sindh": ["Karachi", "Hyderabad"],
        "Punjab": ["Lahore", "Faisalabad", "Multan"],
        "KPK": ["Peshawar", "Abbottabad"],
    }
}


class UserAddress(forms.Form):
    country = forms.ChoiceField(
        choices=[('', '--Select Country--')] + [(c, c) for c in location_data.keys()],
        required=True,
        error_messages={'required': 'Please select your country'}
    )
    state = forms.ChoiceField(
        choices=[('', '--Select State--')],
        required=True,
        error_messages={'required': 'Please select your state'}
    )
    city = forms.ChoiceField(
        choices=[('', '--Select City--')],
        required=True,
        error_messages={'required': 'Please select your city'}
    )

    first_name = forms.CharField(max_length=50, min_length=2, required=True)
    last_name = forms.CharField(max_length=50, min_length=2, required=True)
    mobile = forms.CharField(max_length=10, min_length=10, required=True)
    pincode = forms.CharField(max_length=6, min_length=6, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)
    landmark = forms.CharField(required=False)
    alternative_mobile = forms.CharField(required=False)


# ✅ New Custom Registration Form
class CustomUserCreationForm(UserCreationForm):
    ACCOUNT_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'account_type']


class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, help_text="Enter the 6-digit code sent to your email")


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email address'}),
        help_text="Enter the email address you used to register your account"
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email


class VerifyResetCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6, 
        min_length=6, 
        help_text="Enter the 6-digit reset code sent to your email",
        widget=forms.TextInput(attrs={'placeholder': '000000'})
    )


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        help_text="Password must be at least 8 characters long",
        min_length=8
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        help_text="Enter the same password as before, for verification"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['preferred_currency']
        widgets = {
            'preferred_currency': forms.Select(attrs={'class': 'form-control'})
        }
