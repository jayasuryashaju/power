from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from analytics.models import Visitor
from product.models import Vendor, Category, Product, Variation, Bike
from django.db.models import Q



def increment_daily_visit_count():
    today = timezone.now().date()
    visitor, created = Visitor.objects.get_or_create(date=today)
    visitor.visit_count += 1

    # Set the incremented count in the database
    visitor.save()
    
def get_products_for_category_and_children(category):
    # Base case: return the category itself
    q_objects = Q(category=category)

    # Recursive case: include child categories
    for child_category in Category.objects.filter(parent_category=category):
        q_objects |= get_products_for_category_and_children(child_category)

    return q_objects

def homepage(request):
    user_data = None
    increment_daily_visit_count()
    vendors = []
    categories=[]
    products=[]
    new_products=[]
    featured_products=[]
    banner1_category=[]
    banner2_category=[]
    

    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
        
    vendors = Vendor.objects.all()
    products = Product.objects.all()


    # Retrieve up to four categories 
    categories = Category.objects.all()
    # Fetching categories for banner1 with is_featured=True
    banner1_category = Category.objects.filter(is_featured=True)[:2]

    # Fetching categories for banner2 with is_featured=True
    banner2_category = Category.objects.filter(is_featured=True)[2:4]
    
    featured_products = Product.objects.filter(is_featured=True)[:10]
    new_products = Product.objects.order_by('-date_created')[:20]

    # Create context dictionary
    context = {
        'title': 'Homepage',
        'user_data': user_data,
        'categories': categories,
        'banner1_category': banner1_category,
        'banner2_category': banner2_category,
        'vendors': vendors,
        'products':products,
        'featured_products':featured_products,
        'new_products':new_products,
    }

    return render(request, 'index.html', context)



def product_details(request, slug):
    
    user_data = None

    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
    product = get_object_or_404(Product, slug=slug)
    variations = Variation.objects.filter(product=product)
    related_products = product.get_related_products()

    title = product.name
    

    
    context = {
        'title': title,
        'user_data': user_data,
        'product':product,
        'variations': variations,
        'related_products':related_products
    }
    return render(request, 'product_details.html', context)



def category_list(request, slug):
    user_data = None

    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
        
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(get_products_for_category_and_children(category)).distinct()
        title = category.name
        
        
        context = {
        'title': title,
        'user_data': user_data,
        'products':products,
        'category':category
    }

    
    return render(request, 'product_list.html', context)



def vendor_products(request, slug):
    user_data = None

    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
        
        vendor = get_object_or_404(Vendor, slug=slug)
        products = Product.objects.filter(vendor=vendor)
        title = vendor.name
        
        
        context = {
        'title': title,
        'user_data': user_data,
        'products':products,
        'vendor':vendor
    }

    
    return render(request, 'product_list.html', context)
