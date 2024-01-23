from django import forms
from .models import Vendor, Category, Product, Variation, Bike
from django.contrib import admin



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'image']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'parent_category': forms.Select(attrs={'class': 'form-control'}),
        }
        
class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = '__all__'
        
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'


