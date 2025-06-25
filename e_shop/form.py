from django import forms
state_list = [
    ('', '--Select State--'),  
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]

class UserAddress(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'First name'}),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'minimum length should be 2 letters'
        }
    )
    last_name = forms.CharField(
        max_length=50,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Last name'}),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'minimum length should be 2 letters'
        }
    )
    mobile = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'10-digit Mobile number'}),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'Please enter a valid 10-digit Mobile number'
        }
    )
    pincode = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Pincode'}),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'Please enter a valid 6-digit Pincode'
        }
    )
    address = forms.CharField(
        min_length=10,
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Address (Area, Street)',
                'rows': 5,
                'cols': 40,
                'style': 'resize:none;',
            }
        ),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'Please enter a Address with all the Door no., Street, Area'
        }
    )
    city = forms.CharField(
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'District/City/Town/Village'}),
        error_messages={
            'required' : 'Please fill out this field',
            'min_length' : 'Please enter your District/City/Town/Village name'
        }
    )
    state = forms.ChoiceField(
        choices=state_list,
        error_messages={
            'invalid': 'Please select a state',
        }
    )
    landmark = forms.CharField(
        min_length=1,
        required=False,
        widget=forms.TextInput(attrs={'placeholder':'Landmark (Optional)'}),
    )
    alternative_mobile = forms.CharField(
        min_length=1,
        required=False,
        widget=forms.TextInput(attrs={'placeholder':'Alternavtive Mobile (Optional)'}),
    )