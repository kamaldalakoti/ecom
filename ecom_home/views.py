from django.shortcuts import render,get_object_or_404
# from ecom_home.models  import Customer,Products,Product_order,order
from django.urls import reverse
from .models import Item, OrderItem, Order, Address ,Item_by_seller,SellerAccount_requested , CATEGORY,cal_cat
# , UserProfile
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User 
import time
from django.utils import timezone

from .forms import CheckoutForm

from django.views.generic import ListView, DetailView, View

from .forms import NewSellerForm
from .mixins import SellerAccountMixin
from .models import SellerAccount
from django.views.generic.edit import FormMixin

# Create your views here.
# def index(request):
#     context = {
#        "products":Products.objects.all()
#    }
#     return render(request, 'index.html',context )

class indexView(ListView):
    model = Item
    paginate_by = 25
    template_name = "index.html"


def signup1(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
    data = {'form' : form}
    return render(request, 'accounts/signup.html',data)    
def login(request):
    return render(request, 'accounts/login.html' )
def cart(request):
    
    return render(request, 'cart.html')

class productsDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Products, slug)
    product_order = Product_order.objects.create(item=item)
    Order_qs = order.objects.filter(user=request.user, ordered = False )
    if Order_qs.exists():
        Order = Order_qs[0]
        if Order.item.filter(item__slug=product.item.slug).exists():
            Product_order.quantity += 1
            product_order.save() 
    else:   
            ordered_date = timezone.now() 
            order.items.add(Product_order)
            messages.info(request, "This item was added to your cart.")
            return redirect("ecom_home:product", slug=slug)        
# def search(request):
  
    # return render(request, 'products.html')
# 


# class cart(ListView):
#     model = Products
#     paginate_by = 10
#     template_name = "cart.html"

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                # 'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("ecom_home:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            # order = Order.objects.get(user=self.request.user, ordered=False)
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('ecom_home:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                   
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('ecom_hoome:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")
                        return redirect('ecom_home:checkout')

                user = self.request.user
                order_items = order.items.all()
                order_items.update(ordered=True)
                order.save()
                
                messages.success(self.request,'Order Confirmed')
                return redirect('ecom_home:profile')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("ecom_home:order-summary")





# class HomeView(ListView):
#     model = Item
#     paginate_by = 10
#     template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    
    def get(self, *args, **kwargs):
        try:
            object_list = Item.objects.all()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'object_list' : object_list
            }
            
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecom_home:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("ecom_home:order-summary")
            # return redirect("ecom_home:product")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        # return redirect("ecom_home:product")
        return redirect("ecom_home:order-summary")


@login_required
def profile(request):
    # data1 = 
    # data = Address.objects.get(user=request.user)
    data2 = Address.objects.filter(user=request.user)
    # print(data) 
    print(data2)
    
    info = { 'data2': data2 }
    return render(request, 'account/profile.html' , info)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("ecom_home:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecom_home:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ecom_home:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("ecom_home:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecom_home:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ecom_home:product", slug=slug)
#seller  

class SellerDashboard(SellerAccountMixin, FormMixin,View):
	form_class = NewSellerForm
	success_url = "/profile/"

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get(self, request, *args, **kwargs):
		apply_form = self.get_form() #NewSellerForm()
		account = self.get_account()
		exists = account
		active = None
		context = {}
		if exists:
			active = account.active
		if not exists and not active:
			context["title"] = "Apply for Account"
			context["apply_form"] = apply_form
		elif exists and not active:
			context["title"] = "Account Pending"
		elif exists and active:
			context["title"] = "Seller Dashboard"
			# context["products"] = self.get_products()
			# transactions_today = self.get_transactions_today()
			# context["transactions_today"] = transactions_today
			# context["today_sales"] = self.get_today_sales()
			# context["total_sales"] = self.get_total_sales()
			# context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
		else:
			pass

		return render(request, "account/dashboard.html", context)

	def form_valid(self, form):
		valid_data = super(SellerDashboard, self).form_valid(form)
		obj = SellerAccount.objects.create(user=self.request.user)
		return valid_data

#seller  
@login_required  
def seller_product_post(request):
    object_list = CATEGORY.objects.all()
    data = {'object_list': object_list}
    if request.method == 'POST':
        slug_by_seller  = request.POST.get('slug_by_seller')
        # user_email  = request.POST.get('user_email')
        if Item.objects.filter(slug=slug_by_seller).exists() or Item_by_seller.objects.filter(slug_by_seller=slug_by_seller).exists():
            messages.warning(request, 'Product id is userd try somthing else ' )

            return render(request, 'seller_product_post.html')
            
        else :
        # def clean_username(self):
            # user_email = self.cleaned_data['user_email']
            seller = SellerAccount.objects.get(user__username=request.user)
            title_by_seller  = request.POST.get('title_by_seller')
            Category1  = request.POST.get('category') 
            Category = CATEGORY.objects.get(id = Category1)
            price_by_seller1  = request.POST.get('price_by_seller')
            price_by_seller = float(price_by_seller1)
            discount_price_by_seller  = request.POST.get('discount_price_by_seller')
            discount_price_by_seller = float(discount_price_by_seller)
            # slug_by_seller  = request.POST.get('slug_by_seller')
            description_by_seller  = request.POST.get('description_by_seller')
            image_by_seller  = request.POST.get('image_by_seller')

            seller_product_post = Item_by_seller(title_by_seller= title_by_seller,  price_by_seller= price_by_seller, discount_price_by_seller=discount_price_by_seller, slug_by_seller=slug_by_seller, description_by_seller=description_by_seller,image_by_seller=image_by_seller,seller=seller, Category =Category)
            seller_product_post.save()
            messages.success(request, ' Submition Successfull')
            # return render(request, 'profile.html')

    return render(request, 'seller_product_post.html', data )
@login_required
@user_passes_test(lambda u: u.is_superuser)
def review_seller_product(request):
    seller_item = Item_by_seller.objects.all()
    data = {'seller_item' : seller_item }
    if request.method == 'POST':
        check1 =  request.POST.get('approve')
        # check2 =  request.POST.get('approve1')
        check3 =  request.POST.get('A')
        check4 =  request.POST.get('B')
        check5 =  request.POST.get('C')
        check6 =  request.POST.get('D')
        check7 =  request.POST.get('E')
        check8 =  request.POST.get('F')
        check9 =  request.POST.get('G')
        check10  =  request.POST.get('H')
        check11  =  request.POST.get('I')
        check2  = request.POST.get('J') 
        print(check2)
        # check44 = SellerAccount.objects.get(id)  
        # check44 == check3  
        if check1 == 'True' :
            



            print(check3,check4,check5,check6,check7,check8,check9,check10)
            Category1 = CATEGORY.objects.get(id = check2)
            seller1 = SellerAccount.objects.get(id = check10)
            
            Item.objects.get_or_create(
            seller=seller1,
            seller_username=check3,
            title=check4,
            price=check5,
            discount_price=check6,
            slug=check7,
            description=check8,
            image=check9 ,
            Category=Category1
                )
           
            ABC = Item_by_seller.objects.get(id = check11)
            ABC.delete()
           
          
            messages.success(request, ' Submition Successfull')
            return redirect(reverse('ecom_home:review_seller_product'))
    return render(request, 'review_seller_product.html', data )    
# def tests(request):
#     if request.method == 'POST':
#         check1 =  request.POST.get('approve')
#         print("kamal")
#         if check1 == True :
#             print('hello')
#             messages.success(request, ' Submition Successfull')
#     return render(request, 'review_seller_product.html')
def be_seller(request):
    seller = user=request.user
    seller1 = user=request.user.id
    # print(seller1)
    if SellerAccount.objects.filter(user=seller).exists():
        messages.warning(request,'seller already exists')
        return redirect('/profile')
    elif SellerAccount_requested.objects.filter(user=seller).exists():
        messages.warning(request,"account is panding")
    else :
        if request.method == 'POST':

            name = request.POST.get('seller_name')
            seller2 = User.objects.get(id = seller1)
            print(name)
            SellerAccount_requested.objects.get_or_create(
                user=seller2,
                name=name
                
                    )
            messages.warning(request,'REQUEST SUBMITED')

            print(seller)
    # print(name)
     
    return render(request, 'sellers_index.html')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def be_seller_approve(request):
    seller_ac =  SellerAccount_requested.objects.all()
    data = {'seller_ac' : seller_ac }
    if request.method == 'POST':
        check1 =  request.POST.get('approve')
        # check2 =  request.POST.get('approve1')
        check1 =  request.POST.get('AB')
        check2 =  request.POST.get('AID')
        check3 =  request.POST.get('BID')
        print(check2)
        seller2 = User.objects.get(id = check2)
        # seller3 = SellerAccount_requested.objects.get(id = check3)
        SellerAccount.objects.get_or_create(
            user=seller2,
            name = check1
            
                )
        ABC = SellerAccount_requested.objects.get(id = check3)
        ABC.delete()        
        messages.warning(request,'REQUEST SUBMITED')    
    return render(request, 'seller_ac_approve.html' , data)    

def sell_with_us(request):

    return render(request, 'sell_with_us.html')     
def calculater(request):
    data = cal_cat.objects.all()
    # print(data)



    return render(request, 'calculater.html', {'data':data})     