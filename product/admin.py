from django.contrib import admin
from django.utils.html import mark_safe
from .models import Vendor, Category, Product, Variation


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'slug')
    search_fields = ['name']

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return None

    display_image.short_description = 'Image'

admin.site.register(Vendor, VendorAdmin)

admin.site.register(Category)

admin.site.register(Variation)


admin.site.register(Product)
