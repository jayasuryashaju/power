from product.models import Category, Vendor
from powerenoughadmin.models import Owner  

def add_user_data_to_context(request):
    user_data = None
    if request.user.is_authenticated:
        user_data = {
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }

    # Fetch the Owner instance
    owner = Owner.objects.first()  # Adjust the query as needed to fetch the desired Owner instance

    featured_categories = Category.objects.filter(is_featured=True)[:3]
    categories = Category.objects.all()
    top_level_categories = categories.filter(parent_category__isnull=True)
    vendors = Vendor.objects.all()

    return {
        'user_data': user_data,
        'owner': owner,  # Pass the owner instance to the context
        'featured_categories': featured_categories,
        'categories': categories,
        'top_level_categories': top_level_categories,
        'vendors': vendors,
    }
