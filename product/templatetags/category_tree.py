from django import template
from django.urls import reverse
import locale

register = template.Library()

@register.simple_tag(takes_context=True)
def category_tree(context, category, separator=" > "):
    request = context["request"]
    # Build the absolute URL using reverse
    url = reverse("store:category_list", args=[category.slug])
    # Generate category list
    category_list = [category.name]
    while category.parent_category:
        category = category.parent_category
        category_list.insert(0, category.name)
    return separator.join(category_list)

@register.filter
def inr_format(value):
    try:
        # Set locale to Indian English for currency formatting
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
        value = float(value)
        return locale.format_string("₹%.2f", value, grouping=True)
    except (ValueError, TypeError):
        return value
