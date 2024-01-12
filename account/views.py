# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import User
from .forms import CustomUserForm, SignUpForm, SignInForm
from django.template import loader
from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)





def custom_page_not_found(request, exception):
    return render(request, 'error_404.html', status=404)



def prevent_logged_in_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect the logged-in user to the homepage
            return redirect('store:homepage')
        return view_func(request, *args, **kwargs)

    return _wrapped_view



def user_create(request):
    template_name = 'user_create.html'
    
    try:
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                # Save the form data to create a new user
                # Add your logic here
                messages.success(request, 'User created successfully!')
                return HttpResponseRedirect(reverse('user-list'))
        else:
            form = CustomUserForm()

        return render(request, template_name, {'form': form})
    
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

def user_list(request):
    template_name = 'user_list.html'
    
    try:
        user_list = User.objects.all()
        return render(request, template_name, {'user_list': user_list})
    
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    

def user_edit(request, user_id):
    template_name = 'user_edit.html'
    
    try:
        user = get_object_or_404(User, user_id=user_id)

        if request.method == 'POST':
            form = CustomUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'User updated successfully!')
                return HttpResponseRedirect(reverse('user-list'))
        else:
            form = CustomUserForm(instance=user)

        return render(request, template_name, {'form': form, 'user': user})
    
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

def user_detail(request, user_id):
    template_name = 'user_detail.html'
    
    try:
        user = get_object_or_404(User, user_id=user_id)
        return render(request, template_name, {'user': user})
    
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

def user_delete(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)

        # Handle POST request for deletion
        if request.method == 'POST':
            user.is_active = False
            user.save()
            messages.success(request, 'User deleted successfully!')
            return HttpResponseRedirect(reverse('user-list'))

        # For GET request, delete the user and redirect to the user list
        user.is_active = False
        user.save()
        messages.success(request, 'User deleted successfully!')
        return HttpResponseRedirect(reverse('user-list'))

    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    
    
    
    
    
    
    
    
    
    
    
    
@prevent_logged_in_user
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('store:homepage')
            else:
                messages.error(request, 'Invalid email or password')

    return render(request, 'signin.html', {'title': 'Sign In'})



@prevent_logged_in_user
def signup(request):
    form_signup = SignUpForm()

    if request.method == 'POST':
        form_signup = SignUpForm(request.POST)
        if form_signup.is_valid():
            user = form_signup.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('store:homepage')

    return render(request, 'signup.html', {'form_signup': form_signup, 'title': 'Sign Up'})
    
    
def signout(request):

    try:
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('store:homepage')  # Redirect to your home page
    except Exception as e:
        # Log the exception or handle it as needed
        return HttpResponseServerError(f"An error occurred: {e}", content_type="text/plain")

@prevent_logged_in_user
class CustomPasswordResetView(PasswordResetView):
    template_name = 'custom_password_reset.html'
    email_template_name = 'custom_password_reset_email.html'
    subject_template_name = 'custom_password_reset_subject.txt'
    success_url = '/password_reset/done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'custom_password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'
    success_url = '/password_reset/complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'custom_password_reset_complete.html'

def custom_password_reset(request, *args, **kwargs):
    messages.success(request, 'Password reset email sent successfully. Check your inbox.')
    return CustomPasswordResetView.as_view()(request, *args, **kwargs)

def custom_password_reset_done(request, *args, **kwargs):
    return CustomPasswordResetDoneView.as_view()(request, *args, **kwargs)

def custom_password_reset_confirm(request, *args, **kwargs):
    return CustomPasswordResetConfirmView.as_view()(request, *args, **kwargs)

def custom_password_reset_complete(request, *args, **kwargs):
    return CustomPasswordResetCompleteView.as_view()(request, *args, **kwargs)
