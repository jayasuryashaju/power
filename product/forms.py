from django import forms
from .models import Vendor, Category
from django.contrib import admin



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'image']
        
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm

