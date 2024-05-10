from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'account'

urlpatterns = [
    path('create/', views.user_create, name='user-create'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),    
    path('signout/', views.signout, name='signout'),
    path('<str:user_id>/', views.user_edit, name='user-edit'),
    path('<str:user_id>/detail/', views.user_detail, name='user-detail'),
    path('<str:user_id>/delete/', views.user_delete, name='user-delete'),
    path('', views.user_list, name='user-list'),
    
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



