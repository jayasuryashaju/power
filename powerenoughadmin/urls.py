from django.urls import path
from . import views

app_name = 'powerenoughadmin'

urlpatterns = [
    path('', views.adminhome, name='adminhome'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # __________________________________________----------- Owner ----___________________________________---
    
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/add/', views.owner_add, name='owner_add'),
    path('owners/<int:owner_id>/', views.owner_details, name='owner_detail'),
    path('owners/<int:owner_id>/edit/', views.owner_edit, name='owner_edit'),
    path('owners/<int:owner_id>/delete/', views.owner_delete, name='owner_delete'),
    
    
    path('user_create/', views.user_create, name='user_create'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_edit/<uuid:user_id>/', views.user_edit, name='user_edit'),
    path('user_detail/<uuid:user_id>/', views.user_detail, name='user_detail'),
    path('user_delete/<uuid:user_id>/', views.user_delete, name='user_delete'),
    path('user_deactivate/<uuid:user_id>/', views.user_deactivate, name='user_deactivate'),
    path('user_activate/<uuid:user_id>/', views.user_activate, name='user_activate'),
    
    # ______________________________________________________- vendor -______________________________________________
    
    path('vendor/', views.vendor_list, name='vendor_list'),
    path('vendor/create/', views.vendor_create, name='vendor_create'),
    path('vendor/<slug:slug>/', views.vendor_detail, name='vendor_detail'),
    path('vendor/<slug:slug>/edit/', views.vendor_edit, name='vendor_edit'),
    path('vendor/<slug:slug>/delete/', views.vendor_delete, name='vendor_delete'),
    
    
    
    # ____________________________________________________- category -_______________________________________________
    
    
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:slug>/edit/', views.category_edit, name='category_edit'),
    path('category/<slug:slug>/delete/', views.category_delete, name='category_delete'),
    
    
    # ___________________________________________________- bike -_______________________________________________________
    
    
    
    path('bike/', views.bike_list, name='bike_list'),
    path('bike/create/', views.bike_create, name='bike_create'),
    path('bike/<slug:slug>/edit/', views.bike_edit, name='bike_edit'),
    path('bike/<slug:slug>/delete/', views.bike_delete, name='bike_delete'),
    
    
    # ________________________________________________________--import--__________________________________________________________
    
    path('import/', views.import_products, name='import_products'),
    




]
