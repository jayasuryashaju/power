from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
import os
import uuid

def generate_unique_filename(instance, filename):

    ext = os.path.splitext(filename)[1]  # Extract the file extension
    filename_base = f"{uuid.uuid4().hex}"  # Generate a unique base using UUID
    unique_filename = f"{filename_base}{ext}"  # Combine with extension

    return os.path.join(instance.__class__.__name__.lower(), unique_filename)



class Vendor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=generate_unique_filename, blank=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("powerenoughadmin:vendor_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=generate_unique_filename, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('powerenoughadmin:category', args=[self.slug])
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
        
        
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)    
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)


    variations = models.ManyToManyField('Variation', related_name='products')
    description = models.CharField(max_length=255)
    additional_description = models.CharField(max_length=1000)
    
    image1 = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    image2 = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    image3 = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    image4 = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name  
    
    def get_absolute_url(self):
        return reverse('powerenoughadmin:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super().save(*args, **kwargs)
        
    
class Variation(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    varient_details = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Variation")
        verbose_name_plural = _("Variations")

    def __str__(self):
        return self.size 
    

        
