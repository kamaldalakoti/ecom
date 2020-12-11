from django.contrib import admin

from .models import Item, OrderItem, Order, Address, Customer,signup2,UserProfile,SellerAccount,Item_by_seller,SellerAccount_requested,CATEGORY,Display2,cal_cat,seller_address,SUB_CATEGORY,SUB_CATEGORY_Type,SHIPPING_MODE,ORDERS

# from .models import SellerAccount

admin.site.register(SellerAccount),
admin.site.register(seller_address),
admin.site.register(cal_cat),
admin.site.register(SellerAccount_requested),

admin.site.register(Item),
admin.site.register(ORDERS),
admin.site.register(CATEGORY),
admin.site.register(SUB_CATEGORY),
admin.site.register(SUB_CATEGORY_Type),
admin.site.register(SHIPPING_MODE),
admin.site.register(Item_by_seller),
admin.site.register(OrderItem),
admin.site.register(Order),
admin.site.register(Display2),
# admin.site.register(Payment),
# admin.site.register(Coupon),
# admin.site.register(Refund),
admin.site.register(Address),
admin.site.register(UserProfile),
admin.site.register(Customer),
admin.site.register(signup2),

# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)


# make_refund_accepted.short_description = 'Update orders to refund granted'


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user',
#                     'ordered',
#                     'being_delivered',
#                     'received',
#                     # 'refund_requested',
#                     # 'refund_granted',
#                     'shipping_address',
#                     'billing_address',
#                     # 'payment',
#                     # 'coupon'
#                     ]
#     list_display_links = [
#         'user',
#         'shipping_address',
#         'billing_address',
#         # 'payment',
#         # 'coupon'
#     ]
#     list_filter = ['ordered',
#                    'being_delivered',
#                    'received',
                #    'refund_requested',
                #    'refund_granted']
    # search_fields = [
    #     'user__username',
    #     # 'ref_code'
    # ]
    # actions = [make_refund_accepted]


# class AddressAdmin(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'street_address',
#         'apartment_address',
#         # 'country',
#         'zip',
#         'address_type',
#         'default'
#     ]
#     list_filter = ['default', 'address_type' ]
    # search_fields = ['user', 'street_address', 'apartment_address', 'zip']


# admin.site.register(Item),
# admin.site.register(OrderItem),
# admin.site.register(Order, OrderAdmin),
# # admin.site.register(Payment),
# # admin.site.register(Coupon),
# # admin.site.register(Refund),
# admin.site.register(Address, AddressAdmin),
# admin.site.register(UserProfile),

# admin.site.register(Customer),
# admin.site.register(signup2)