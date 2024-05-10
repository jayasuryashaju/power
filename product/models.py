from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from account.models import User
import os
import uuid




def generate_unique_filename(instance, filename):
    ext = os.path.splitext(filename)[1]  # Extract the file extension
    filename_base = uuid.uuid4().hex  # Generate a unique base using UUID
    unique_filename = f"{filename_base}{ext}"  # Combine with extension
    return os.path.join(instance.__class__.__name__.lower(), unique_filename)


class Vendor(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=generate_unique_filename, blank=True)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:vendor_products", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=generate_unique_filename, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    has_offer = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
          
class Bike(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    slug = models.SlugField(unique=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.make} {self.model} {self.start_year}-{self.end_year}")
        super().save(*args, **kwargs)
 
    def __str__(self):
        return f"{self.make} {self.model} {self.start_year}-{self.end_year}"
               
class Product(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)    
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    bikes = models.ManyToManyField(Bike, related_name='products', blank=True)
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    has_offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    additional_description = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name  
    
    def get_absolute_url(self):
        return reverse('store:product_details', args=[self.slug])
    
    def increment_views(self):
        self.view_count += 1
        self.save()
    
    def get_related_products(self, num_related=10):
        """
        Get related products based on common categories.
        Adjust the logic based on your specific criteria.
        """
        # Get all categories of the current product
        current_product_categories = [self.category]

        # Get related products excluding the current product
        related_products = Product.objects.filter(
            category__in=current_product_categories
        ).exclude(id=self.id).distinct()[:num_related]

        return related_products

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super().save(*args, **kwargs)
        
    
        
class ProductImage(models.Model):
    image = models.ImageField(upload_to=generate_unique_filename)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', default=None)  
    alt_text = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.alt_text:
            # Generate alt text using product name and image filename
            product_name = slugify(self.product.name)
            image_name = os.path.splitext(os.path.basename(self.image.name))[0]
            alt_text = f"{product_name} - Image {self.pk} - {image_name}"
            self.alt_text = alt_text.capitalize()  # Capitalize first letter
        super().save(*args, **kwargs)
    
            
class Variation(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations', default=None)
    variant_details = models.TextField(blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255,null=True, blank=True)  
    sku = models.CharField(max_length=255, unique=False, blank=True)
    stock = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Variation")
        verbose_name_plural = _("Variations")

    def __str__(self):
        return f"{self.product.name} - {self.sku} ({self.size}, {self.color})"
    
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        if self.user:
            return f"Review by {self.user.username} for {self.product.name}"
        else:
            return f"Anonymous Review for {self.product.name}"

        
