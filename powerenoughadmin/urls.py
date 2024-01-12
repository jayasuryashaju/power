from django.urls import path
from . import views

app_name = 'powerenoughadmin'

urlpatterns = [
    path('', views.adminhome, name='adminhome'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    
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



]
