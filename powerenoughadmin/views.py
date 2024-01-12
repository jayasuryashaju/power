from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, Http404
from .decorators import admin_required
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseServerError, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import CustomUserForm
from account.models import User
from product.models import  Vendor
from product.forms import VendorForm
from analytics.models import Visitor
from django.utils import timezone




def increment_daily_visit_count():
    today = timezone.now().date()
    visitor, created = Visitor.objects.get_or_create(date=today)
    visitor.visit_count += 1
    visitor.save()

def adminhome(request):
    template_name = 'custom_admin/index.html'

    # Increment visit count when the page is visited
    increment_daily_visit_count()

    # Retrieve all visitor data
    visitors = Visitor.objects.all()
    
    # Extract dates and visit counts
    dates = [visitor.date.strftime('%Y-%m-%d') for visitor in visitors]
    visit_counts = [visitor.visit_count for visitor in visitors]

    return render(request, template_name, {'dates': dates, 'visit_counts': visit_counts})
    
   



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' field is used for email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('powerenoughadmin:adminhome')  
    else:
        form = AuthenticationForm()

    return render(request, 'custom_admin/login.html', {'form': form})

@admin_required
def custom_logout(request):
    try:
        logout(request)
        return redirect('powerenoughadmin:login')  
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {e}", content_type="text/plain")
    
    
    
    
    
@admin_required
def user_create(request):
    template_name = 'custom_admin/user_create.html'
    
    try:
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User created successfully!')
                return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
        else:
            form = CustomUserForm()

        return render(request, template_name, {'form': form})
    
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

@admin_required
def user_list(request):
    template_name = 'custom_admin/user_list.html'
    
    try:
        user_list = User.objects.all()
        
        # Search filter
        query = request.GET.get('q')
        if query:
            user_list = user_list.filter(Q(full_name__icontains=query) | Q(email__icontains=query))

        return render(request, template_name, {'user_list': user_list})
    
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    
    
    

@admin_required
def user_edit(request, user_id):
    template_name = 'custom_admin/user_edit.html'
    
    try:
        user = get_object_or_404(User, user_id=user_id)

        if request.method == 'POST':
            form = CustomUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'User updated successfully!')
                return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
        else:
            form = CustomUserForm(instance=user)

        return render(request, template_name, {'form': form, 'user': user})
    
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    
    

@admin_required
def user_detail(request, user_id):
    template_name = 'user_detail.html'
    
    try:
        user = get_object_or_404(User, user_id=user_id)
        return render(request, template_name, {'user': user})
    
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    
    
@admin_required
def user_deactivate(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)

        if user:
            user.is_active = False
            user.save()
            messages.success(request, 'User updated successfully!')
            return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
        else:
            return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
         
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

    
@admin_required
def user_activate(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)

        if user:
            user.is_active = True
            user.save()
            messages.success(request, 'User updated successfully!')
            return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
        else:
            return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))
         
    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))

@admin_required
def user_delete(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)

        # Handle POST request for soft-deleting
        if request.method == 'POST':
            user.is_active = False
            user.save()
            messages.success(request, 'User deactivated successfully!')
            return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))

        # For GET request, deactivate the user and redirect to the user list
        user.is_active = False
        user.save()
        messages.success(request, 'User deactivated successfully!')
        return HttpResponseRedirect(reverse('powerenoughadmin:user_list'))

    except Http404:
        raise Http404("User not found.")
    except Exception as e:
        return HttpResponseServerError(render(request, 'error_500.html', {'error_message': str(e)}))
    
    
    
    
    
    # __________________________________________________- vendor details  -___________________________________________________________________________
    
@admin_required   
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'custom_admin/vendor_list.html', {'vendors': vendors})

@admin_required 
def vendor_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    return render(request, 'custom_admin/vendor_detail.html', {'vendor': vendor})

@admin_required 
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:vendor_list')
    else:
        form = VendorForm()
    return render(request, 'custom_admin/vendor_form.html', {'form': form})

@admin_required 
def vendor_edit(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'custom_admin/vendor_form.html', {'form': form, 'vendor': vendor})

@admin_required 
def vendor_delete(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    vendor.delete()
    return redirect('powerenoughadmin:vendor_list')