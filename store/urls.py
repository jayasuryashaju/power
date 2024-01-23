from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<slug:slug>', views.product_details, name='product_details'),
    path('category/<slug:slug>', views.category_list, name='category_list'),
    path('vendor/<slug:slug>', views.vendor_products, name='vendor_products'),
]
