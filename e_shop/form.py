from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(label='first name', max_length=50)
    last_name = forms.CharField(label='last name', max_length=50)
    phone_no = forms.IntegerField()
    email = forms.EmailField(error_messages={'required': 'Please enter your name!'})
    message = forms.CharField(widget=forms.Textarea)
    