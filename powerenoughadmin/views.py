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
from .forms import CustomUserForm, OwnerForm
from .models import Owner
from account.models import User
from product.models import  Vendor, Category, Product, Bike, Variation, ProductImage
from product.forms import VendorForm, CategoryForm, ProductForm, VariationForm, BikeForm
from analytics.models import Visitor
from django.utils import timezone
import pandas as pd
from urllib.request import urlretrieve
from .forms import ImportCSVForm
from django.http import JsonResponse
from django.core.files import File
from urllib.request import urlretrieve
from io import BytesIO
import os
from django.db.utils import IntegrityError
from urllib.error import URLError






def increment_daily_visit_count():
    today = timezone.now().date()
    visitor, created = Visitor.objects.get_or_create(date=today)
    visitor.visit_count += 1
    visitor.save()
    
@admin_required
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


def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'custom_admin/owner_list.html', {'owners': owners})

def owner_details(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    return render(request, 'custom_admin/owner_detail.html', {'owner': owner})

def owner_add(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:owner_list')
    else:
        form = OwnerForm()
    return render(request, 'custom_admin/owner_add.html', {'form': form})

def owner_edit(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:owner_detail', owner_id=owner_id)
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'custom_admin/owner_edit.html', {'form': form})

def owner_delete(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    if request.method == 'POST':
        owner.delete()
        return redirect('powerenoughadmin:owner_list')
    return render(request, 'custom_admin/owner_delete.html', {'owner': owner})
    
   



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



# ________________________________________________________- category details - ________________________________________________________________________________




@admin_required   
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/category_list.html', {'categories': categories})

@admin_required 
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'custom_admin/category_detail.html', {'category': category})

@admin_required 
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:category_list')
    else:
        form = CategoryForm()
    return render(request, 'custom_admin/category_form.html', {'form': form})

@admin_required 
def category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'custom_admin/category_form.html', {'form': form, 'category': category})

@admin_required 
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('powerenoughadmin:category_list')







# _______________________________________________________-- bike --________________________________________________________________________________________




@admin_required   
def bike_list(request):
    bikes = Bike.objects.all()
    return render(request, 'custom_admin/bike_list.html', {'bikes': bikes})


@admin_required 
def bike_create(request):
    if request.method == 'POST':
        form = BikeForm(request.POST)
        if form.is_valid():
            print("create bike function is working fine")
            form.save()
            return redirect('powerenoughadmin:bike_list')
    else:
        form = BikeForm()
        print(form)
    return render(request, 'custom_admin/bike_form.html', {'form': form})

@admin_required 
def bike_edit(request, slug):
    bike = get_object_or_404(Bike, slug=slug)
    if request.method == 'POST':
        form = BikeForm(request.POST, instance=bike)
        if form.is_valid():
            form.save()
            return redirect('powerenoughadmin:bike_list')
    else:
        form = BikeForm(instance=bike)
    return render(request, 'custom_admin/bike_form.html', {'form': form, 'bike': bike})

@admin_required 
def bike_delete(request, slug):
    bike = get_object_or_404(Bike, slug=slug)
    bike.delete()
    return redirect('powerenoughadmin:bike_list')




#--------------------------------------------------- import-----------------------------------------------------


def download_image(image_url):
    try:
        # Download the image from the URL
        filename, headers = urlretrieve(image_url)
        with open(filename, 'rb') as file:
            image_content = BytesIO(file.read())

        # Get the filename from the URL
        filename = os.path.basename(image_url)

        # Create a Django File object from the image content
        image_file = File(image_content, name=filename)

        return image_file

    except (URLError, FileNotFoundError) as e:
        # Handle errors during image download
        print(f"Error downloading image from {image_url}: {e}")
        return None
    

def import_products(request):
    if request.method == 'POST':
        form = ImportCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            for index, row in df.iterrows():
                if not pd.isna(row['Product Name']):  # Skip rows where 'Product Name' is NaN
                    try:
                        # Check if the vendor exists, if not create it
                        vendor_name = row['Vendor']
                        vendor, created = Vendor.objects.get_or_create(name=vendor_name)

                        # Check if the category exists, if not create it
                        category_name = row['Category']
                        category, created = Category.objects.get_or_create(name=category_name)

                        # # Handle NaN values in prices
                        # new_price = row['New Price']
                        # old_price = row['Old Price']
                        # if pd.isna(new_price) and pd.isna(old_price):
                        #     price = 0.00
                        #     has_offer = False
                        #     offer_price = None
                        # else:
                        #     if pd.notna(old_price):
                        #         price = old_price
                        #         if pd.notna(new_price):
                        #             has_offer = True
                        #             offer_price = new_price
                        #         else:
                        #             has_offer = False
                        #             offer_price = None
                        #     else:
                        #         price = new_price
                        #         has_offer = False
                        #         offer_price = None
                        price = 100
                        has_offer = False
                        offer_price = None

                        # Create the product
                        product = Product.objects.create(
                            name=row['Product Name'],
                            category=category,
                            vendor=vendor,
                            description=row['Description'],
                            # additional_description=row['Additional Description'],
                            price=price,
                            has_offer=has_offer,
                            offer_price=offer_price
                        )

                        # Download and associate images
                        images = eval(row['Images'])  # Convert string representation to list
                        is_first_image = True  # Flag to track the first image
                        for i, image_url in enumerate(images):
                            # Download the image and create a File object
                            image_file = download_image(image_url)

                            if image_file is not None:
                                # Set is_featured to True for the first image
                                is_featured = is_first_image
                                is_first_image = False

                                # Create a ProductImage object
                                product_image = ProductImage.objects.create(
                                    product=product,
                                    image=image_file,  # Pass the File object to the image field
                                    is_featured=is_featured  # Set is_featured field
                                    # Add more fields as needed
                                )
                            else:
                                # Skip this image and continue to the next one
                                continue

                        # Add variations
                        variations = []
                        if 'Sizes SKUs' in row:
                            sizes_skus_data = eval(row['Sizes SKUs'])  # Assuming 'Sizes SKUs' column contains variation data
                            for size, sku in sizes_skus_data.items():
                                variation = Variation(
                                    product=product,
                                    size=size,
                                    sku=sku,
                                    stock=10  # Set initial stock, adjust as needed
                                    # Add more variation fields as needed
                                )
                                variations.append(variation)
                        Variation.objects.bulk_create(variations)

                        # After adding each product, you can print a message
                        print(f"Product {row['Product Name']} added successfully")

                    except IntegrityError:
                        # Handle the case where a product with the same name already exists
                        print(f"Product {row['Product Name']} already exists. Skipping...")

            return JsonResponse({'success': True, 'message': 'Products added successfully'})
    else:
        form = ImportCSVForm()
    return render(request, 'custom_admin/import_products.html', {'form': form})
