from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if confirm_password != password:
            self.add_error('confirm_password', 'Passwords do not match each other')
        
        if username:
            if not any(char.isdigit() for char in username):
                self.add_error('username', 'username must contain a number')
    
    
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)