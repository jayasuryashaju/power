from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<slug:slug>', views.product_details, name='product_details'),
    path('category/<slug:slug>', views.category_list, name='category_list'),
    path('vendor/<slug:slug>', views.vendor_products, name='vendor_products'),
    path('fetch-makes/', views.fetch_makes, name='fetch_makes'),
    path('fetch-models/', views.fetch_models, name='fetch_models'),
    path('fetch-years/', views.fetch_years, name='fetch_years'),
    path('bike_products/', views.bike_products, name='bike_products'),
    path('search/', views.search_products, name='search_products'),
    path('contact_form/', views.contact_form, name='contact_form'),
]
