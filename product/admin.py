from django.contrib import admin
from django.utils.html import mark_safe
from .models import Vendor, Category, Product, Variation, ProductImage, Bike
from django.utils.html import format_html
from django.urls import reverse



class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'slug')
    search_fields = ['name']

    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return None

    display_image.short_description = 'Image'

admin.site.register(Vendor, VendorAdmin)


# admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'has_offer', 'is_featured')
    search_fields = ('name',)
    list_filter = ('parent_category',)

    def parent_category(self, obj):
        return obj.parent_category.name if obj.parent_category else None

    parent_category.short_description = 'Parent Category'

    def tree_actions(self, obj):
        actions = format_html('<a href="{}">View</a>', reverse('powerenoughadmin:category_detail', args=[obj.slug]))
        return actions

    tree_actions.short_description = 'Actions'

admin.site.register(Category, CategoryAdmin)


admin.site.register(Bike)




class VariationInline(admin.StackedInline):
    model = Variation
    extra = 1  #
class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1  
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vendor')
    readonly_fields = ('slug',)
    inlines = [VariationInline, ProductImageInline]

admin.site.register(Product, ProductAdmin)
 

