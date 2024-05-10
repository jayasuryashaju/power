from django.db import models

class Owner(models.Model):
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    website_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    footer_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    whatsapp = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Add any additional fields or methods here

    def __str__(self):
        return self.email  # Or any other field you want to display as the owner's representation
