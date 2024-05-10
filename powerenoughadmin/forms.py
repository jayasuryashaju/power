from django import forms
from account.models import User
from .models import Owner
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'phone_number', 'password1', 'password2')

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'phone_number', 'is_active')


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['email', 'address', 'city', 'country', 'favicon', 'website_logo', 'footer_logo', 'whatsapp', 'instagram', 'youtube', 'twitter', 'phone_number']
        labels = {
            'email': 'Email',
            'address': 'Address',
            'city': 'City',
            'country': 'Country',
            'favicon': 'Favicon',
            'website_logo': 'Website Logo',
            'footer_logo': 'Footer Logo',
            'whatsapp': 'WhatsApp',
            'instagram': 'Instagram',
            'youtube': 'YouTube',
            'twitter': 'Twitter',
            'phone_number': 'Phone Number',
        }

        
class ImportCSVForm(forms.Form):
    csv_file = forms.FileField(label='Select CSV File')
            
