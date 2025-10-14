from django import template

register = template.Library()

@register.filter
def in_wishlist(product, user):
    if user.is_authenticated:
        return product.wishlisted_by.filter(user=user).exists()
    return False
