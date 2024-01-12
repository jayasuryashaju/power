from django.shortcuts import render
from django.utils import timezone
from analytics.models import Visitor
from product.models import Vendor, Category
from django.db.models import Q



def increment_daily_visit_count():
    today = timezone.now().date()
    visitor, created = Visitor.objects.get_or_create(date=today)
    visitor.visit_count += 1

    # Set the incremented count in the database
    visitor.save()

def homepage(request):
    user_data = None
    increment_daily_visit_count()

    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
        
    vendors = Vendor.objects.all()


    # Retrieve up to four categories (customize the query as needed)
    categories = Category.objects.all()
    banner1_category = Category.objects.filter(Q(name='Helmets') | Q(name='Exhausts'))
    banner2_category = Category.objects.filter(Q(name='Jackets') | Q(name='Gloves'))

    # Create context dictionary
    context = {
        'title': 'Homepage',
        'user_data': user_data,
        'categories': categories,
        'banner1_category': banner1_category,
        'banner2_category': banner2_category,
        'vendors': vendors,
    }

    return render(request, 'index.html', context)
