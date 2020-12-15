from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Item, OrderItem, Order, Address ,Item_by_seller,SellerAccount_requested , CATEGORY,cal_cat,seller_address,SUB_CATEGORY,SUB_CATEGORY_Type,SHIPPING_MODE,ORDERS,SellerAccount


def seller_active(view_func):
    def wrap(request, *args, **kwargs):
        if SellerAccount.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            messages.info(request, "Not ativated account.")
            return redirect("/seller_account") 
    return wrap


# decorators

# @login_required
# def seller_active(request):
#     user = request.user
#     if SellerAccount.objects.filter(user=user).exists():
#         pass
#     else:
#         messages.info(request, "Not ativated account.")
#         return redirect("ecom_home:seller_account")           
