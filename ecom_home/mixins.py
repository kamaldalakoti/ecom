import datetime
from django.db.models import Count, Min, Sum, Avg, Max
# from billing.models import Transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# from djangodm.mixins import LoginRequiredMixin
from .models import Item

from .models import SellerAccount

from django.http import Http404

# from djangodm.mixins import LoginRequiredMixin
# from sellers.mixins import SellerAccountMixin

# Seller account mixins

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class SellerAccountMixin(LoginRequiredMixin, object):
	account = None
	productsz = []
	transactions = []

	def get_account(self):
		user = self.request.user
		accounts = SellerAccount.objects.filter(user=user)
		if accounts.exists() and accounts.count() == 1:
			self.account = accounts.first()
			return accounts.first()
		return None

	# def get_products(self):
	# 	account = self.get_account()
	# 	products = Item.objects.filter(seller=account)
	# 	self.products = products
	# 	return products

	# def get_transactions(self):
	# 	products = self.get_products()
	# 	transactions = Transaction.objects.filter(product__in=products)
	# 	return transactions

	# def get_transactions_today(self):
	# 	today = datetime.date.today()
	# 	today_min = datetime.datetime.combine(today, datetime.time.min)
	# 	today_max = datetime.datetime.combine(today, datetime.time.max)
	# 	# print today, today_min, today_max
	# 	return self.get_transactions().filter(timestamp__range=(today_min, today_max))

	# def get_total_sales(self):
	# 	transactions = self.get_transactions().aggregate(Sum("price"))
	# 	total_sales = transactions["price__sum"]
	# 	return total_sales

	# def get_today_sales(self):
	# 	transactions = self.get_transactions_today().aggregate(Sum("price"), Avg("price"))
	# 	total_sales = transactions["price__sum"]
	# 	return total_sales

class ProductManagerMixin(SellerAccountMixin, object):
    def get_object(self, *args, **kwargs):
        seller = self.get_account()
        obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
        try:
            obj.seller == seller
        except:
            raise Http404
        if obj.seller == seller:
            return obj
        else:
            raise Http404
