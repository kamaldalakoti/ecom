from django import template
from ecom_home.models import Order,Address

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

# @register.filter
# def address_book(user ):
#     if user.is_authenticated:
#         ad = Address.objects.filter(user=user)
#         return ad
#     return 0