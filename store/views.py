from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from analytics.models import Visitor
from product.models import Vendor, Category, Product, Variation, Bike
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail





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
    increment_daily_visit_count()
    vendors = []
    categories=[]
    products=[]
    new_products=[]
    featured_products=[]
    banner1_category=[]
    banner2_category=[]
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    


    banner1_category = Category.objects.filter(is_featured=True)[:2]
    banner2_category = Category.objects.filter(is_featured=True)[2:4]
    
    featured_products = Product.objects.filter(is_featured=True)[:10]
    new_products = Product.objects.order_by('-date_created')[:10]


    # Create context dictionary
    context = {
        'title': 'Homepage',
        'categories': categories,
        'banner1_category': banner1_category,
        'banner2_category': banner2_category,
        'vendors': vendors,
        'new_products':new_products,
        'featured_products':featured_products,
        'new_products':new_products,
    }

    return render(request, 'index.html', context)


def fetch_makes(request):
    makes = Bike.objects.values_list('make', flat=True).distinct()
    return JsonResponse(list(makes), safe=False)

def fetch_models(request):
    make = request.GET.get('make')
    models = Bike.objects.filter(make=make).values_list('model', flat=True).distinct()
    return JsonResponse(list(models), safe=False)

def fetch_years(request):
    make = request.GET.get('make')
    model = request.GET.get('model')
    years = Bike.objects.filter(make=make, model=model).values_list('start_year', 'end_year')
    years_list = []
    for start_year, end_year in years:
        years_list.extend(list(range(start_year, end_year + 1)))
    return JsonResponse(years_list, safe=False)


def bike_products(request):
   
    if request.method == 'GET':
        make = request.GET.get('make')
        model = request.GET.get('model')
        year = request.GET.get('year')
        if not all([make, model, year]):
            return HttpResponseBadRequest("Make, model, and year parameters are required.")

        bike = Bike.objects.filter(make=make, model=model, start_year__lte=year, end_year__gte=year).first()

        if bike:
            title = bike.make + " " +  bike.model
            products = Product.objects.filter(bikes=bike)
            
            
            context = {
                        'title': title,
                        'products':products,
                        'bike':bike
                    }
            return render(request, 'product_list.html', context)
        else:
            context = {
                    'title': title,
                }
            return render(request, 'product_list.html', context)


def product_details(request, slug):

    product = get_object_or_404(Product, slug=slug)
    product.view_count += 1
    product.save()
    variations = Variation.objects.filter(product=product)
    related_products = product.get_related_products()

    title = product.name
    

    
    context = {
        'title': title,
        'product':product,
        'variations': variations,
        'related_products':related_products
    }
    return render(request, 'product_details.html', context)



def category_list(request, slug):
    
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(get_products_for_category_and_children(category)).distinct()
        title = category.name
        
        # Pagination
        paginator = Paginator(products, 20)  
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)
        
        context = {
            'title': title,
            'products': page_obj,  
            'category': category
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
      
    # Pagination
    paginator = Paginator(products, 20)  # Change 10 to the desired number of items per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    context = {
        'title': title,
        'user_data': user_data,
        'products': page_obj,
        'vendor': vendor
    }

    return render(request, 'product_list.html', context)



def search_products(request):
    """
    View function for handling search requests.
    """
    query = request.GET.get('q')
    if query:
        # Perform search
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(additional_description__icontains=query) |
            Q(bikes__make__icontains=query) |  # Search in bike make
            Q(bikes__model__icontains=query)    # Search in bike model
        ).distinct()
        title = f"Search results for '{query}'"
    else:
        # If no query provided, return an empty queryset
        products = Product.objects.none()
        title = "Search results"

    # Pagination
    paginator = Paginator(products, 20)  # Change 20 to the desired number of items per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'products': page_obj,
    }

    return render(request, 'product_list.html', context)




def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            'email',  # Change this to your email address
            # ['powerenough76@gmail.com'],  # Change this to the recipient's email address
            ['jayasuryashaju3031@gmail.com'],
            fail_silently=False,
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})