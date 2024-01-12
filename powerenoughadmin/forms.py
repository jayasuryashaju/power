from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    # You can customize this form further if needed
    pass


from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'phone_number', 'password1', 'password2')

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'phone_number', 'is_active')
