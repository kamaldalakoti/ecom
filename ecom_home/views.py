from django.shortcuts import render,get_object_or_404
# from ecom_home.models  import Customer,Products,Product_order,order
from django.urls import reverse
from .models import Item, OrderItem, Order, Address ,Item_by_seller,SellerAccount_requested , CATEGORY,cal_cat,seller_address,SUB_CATEGORY,SUB_CATEGORY_Type,SHIPPING_MODE,ORDERS
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

# firebase 


# default_app = firebase_admin.initialize_app()
# config = {
#     "apiKey": "AIzaSyB2dcKOFsNIcAc0yOGAvMaNCcaVRYe4Fq8",
#     "authDomain": "protean-sensor-278302.firebaseapp.com",
#     "databaseURL": "https://ecom-c8c63-default-rtdb.firebaseio.com/",
#     "projectId": "protean-sensor-278302",
#     "storageBucket": "protean-sensor-278302.appspot.com",
#     "serviceAccount": "static\protean-sensor-278302-firebase-adminsdk-c67u8-e63e2fd2dc.json",
#     "messagingSenderId": "111376756390"
# }
# # 
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# firebase 


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
def signup(request):
    return render(request, 'accounts/signup.html' )
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


class cart(ListView):
    model = Item
    paginate_by = 10
    # template_name = "cart.html"
    template_name = "order_snippet.html"

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)
def testadd(request):
    add_data = ORDERS.objects.filter(user=request.user)
    print(add_data)
    return render(request, 'testadd.html',{'add_data':add_data})

def checkout(request):
    address_data = Address.objects.filter(user=request.user)
    order_item_data = OrderItem.objects.filter(user=request.user)
    
    if request.method == 'POST' and 'Order_submit' in request.POST:
        item1 = request.POST.get('Check')
        if item1 != None :
            order_item = OrderItem.objects.get(id = item1)
            seller_ID = order_item.item.seller.id 
            item = order_item.item.id 
            quantity = order_item.quantity
            print(seller_ID)
            # seller_ID = request.POST.get('seller_ID')
            seller = SellerAccount.objects.get(id = seller_ID)
            user_id = request.user
            # item = request.POST.get('item')
            item = Item.objects.get(id = item)
            # quantity = request.POST.get('quantity')
            street_address = request.POST.get('street_address')
            apartment_address = request.POST.get('apartment_address')
            landmark = request.POST.get('landmark')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            zip_code = request.POST.get('zip_code')
            
            print(item1)
            # print(item)
            # print('hello')
            Add_orders = ORDERS(seller = seller , user = user_id , item = item , quantity = quantity , street_address = street_address , apartment_address = apartment_address , landmark= landmark, city = city,state = state , country = country , zip_code = zip_code 
                )
            Add_orders.save()
            order_item_delete = OrderItem.objects.get(id = item1)
            order_item_delete.delete()
        else : 
            messages.info(request, "You do not have an active order")
            return redirect('/checkout1')
    elif request.method == 'POST' and 'Address_submit' in request.POST:
        ID = request.POST.get('ID')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        if Address.objects.filter(user=request.user).exists():
            ADD =  Address.objects.get(id= ID)
            ADD.street_address = street_address
            ADD.apartment_address = apartment_address
            ADD.landmark = landmark
            ADD.city = city 
            ADD.state = state
            ADD.country = country
            ADD.zip_code = zip_code
            ADD.save()
            print(ADD)

            
            messages.info(request, "Address Updated")
            redirect('ecom_home:checkout')
        else:
            ADD_Address =     Address(user=request.user, street_address = street_address,apartment_address = apartment_address,landmark = landmark,city = city,state = state,country = country,zip_code = zip_code ,)
            ADD_Address.save()
            messages.info(request, "Address saved")
            redirect('ecom_home:checkout')

       

    return render(request, 'product_order/checkout.html' ,{'address_data':address_data , 'order_item_data':order_item_data })
@login_required
def profile(request):
    add_data = Address.objects.filter(user=request.user)
    print(add_data)
    
    return render(request, 'account/profile.html' , {'add_data':add_data})
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

# 
@login_required
def dashboard(request):
    seller = user = request.user
    # seller1 = user = request.user.id
    # print(seller1)
    context = {}
    context = {'name' : seller}

    if SellerAccount.objects.filter(user=seller).exists():
        context["data"] = "Activeted"
        return render(request, "account/dashboard.html", context)

        
    elif SellerAccount_requested.objects.filter(user=seller).exists():
        context["data"] = "Account Pending"

    elif not SellerAccount_requested.objects.filter(user=seller).exists() and not SellerAccount.objects.filter(user=seller).exists() :
        context["data"] = "Not registered"

        return render(request, "account/dashboard.html", context)
        
    else:
        return render(request, "account/dashboard.html", context)
    return render(request, "account/dashboard.html", context)

#seller  
@login_required  
def seller_product_post(request , Type):
    object_list3 = SUB_CATEGORY_Type.objects.get(id=Type)
    object_list4 = SHIPPING_MODE.objects.all()
    
    # object_list = CATEGORY.objects.all()
    # object_list1 = SUB_CATEGORY.objects.all()
    # object_list2 = SUB_CATEGORY_Type.objects.all()
    data = {'object_list3': object_list3 , 'object_list4': object_list4}
    seller = user = request.user
    if SellerAccount.objects.filter(user=seller).exists():
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
                Category1  = request.POST.get('Category') 
                Sub_Category1  = request.POST.get('Sub_Category') 
                Type1  = request.POST.get('Type') 
                Category = CATEGORY.objects.get(id = Category1)
                Sub_Category = SUB_CATEGORY.objects.get(id = Sub_Category1)
                Type = SUB_CATEGORY_Type.objects.get(id = Type1)
                price_by_seller1  = request.POST.get('price_by_seller')
                price_by_seller = float(price_by_seller1)
                discount_price_by_seller  = request.POST.get('discount_price_by_seller')
                discount_price_by_seller = float(discount_price_by_seller)
                # slug_by_seller  = request.POST.get('slug_by_seller')
                description_by_seller  = request.POST.get('description_by_seller')
                image_by_seller  = request.POST.get('image_by_seller')
                Brand = request.POST.get('Brand')
                MRP = request.POST.get('MRP')
                Pincode_pro = request.POST.get('Pincode_pro')
                Seller_SKU = request.POST.get('Seller_SKU')
                Produt_tax_code = request.POST.get('Produt_tax_code')
                Shipping_Mode1 = request.POST.get('Shipping_Mode')
                Shipping_Mode = SHIPPING_MODE.objects.get(id = Shipping_Mode1)
                
                seller_product_post = Item_by_seller(title_by_seller= title_by_seller, Category= Category , Sub_Category = Sub_Category ,Type=Type,  Brand= Brand, MRP=MRP,  price_by_seller= price_by_seller,Pincode_pro=Pincode_pro, Shipping_Mode=Shipping_Mode  ,discount_price_by_seller=discount_price_by_seller, Seller_SKU=Seller_SKU, Produt_tax_code=Produt_tax_code, slug_by_seller=slug_by_seller, description_by_seller=description_by_seller,image_by_seller=image_by_seller,seller=seller)
                seller_product_post.save()
                messages.success(request, ' Submition Successfull')
                # return render(request, 'profile.html')
    else:
        messages.info(request, "First fill your tax info")
        return redirect("/dashboard")

    return render(request, 'PRODUCT_LISTING/seller_product_post.html' , data )

def Category(request ):
    object_list = CATEGORY.objects.all()
    
    data = {'object_list' : object_list }
    if request.method == 'POST':
        cat = request.POST.get('category')
        # print(cat)  
        # return redirect("/Sub_Category")
            
    return render(request, 'category\category.html', data )      
def Sub_Category(request, Category ):
    
    
    object_list1 = CATEGORY.objects.get(id=Category)
    object_list = SUB_CATEGORY.objects.filter(Category=Category)
    # object_list = SUB_CATEGORY.objects.all(  )
    
    data = {'object_list' : object_list , 'object_list1' : object_list1}
    

             
    return render(request, 'category\sub_category\sub_category.html', data    )      
def Type(request , Sub_Category ): 
    object_list2 = SUB_CATEGORY.objects.get(id=Sub_Category)
    object_list = SUB_CATEGORY_Type.objects.filter(Sub_Category=Sub_Category)
    # object_list = SUB_CATEGORY.objects.all(  )
    
    data = {'object_list' : object_list , 'object_list2' : object_list2  }
    

            
    return render(request, 'category\\sub_category\\type\\type.html', data , )      
@login_required
# @user_passes_test(lambda u: u.is_superuser)

def review_seller_product(request , slug_by_seller):
    seller_item = Item_by_seller.objects.get(slug_by_seller=slug_by_seller)
    
    data = {'object' : seller_item  }
    if request.method == 'POST':
        check1 =  request.POST.get('approve')
        
        seller =  request.POST.get('seller')
        title_by_seller =  request.POST.get('title_by_seller')
        price_by_seller =  request.POST.get('price_by_seller')
        discount_price_by_seller =  request.POST.get('discount_price_by_seller')
        slug_by_seller11 =  request.POST.get('slug_by_seller11')
        description_by_seller =  request.POST.get('description_by_seller')
        image_by_seller =  request.POST.get('image_by_seller')
        seller_id  =  request.POST.get('seller_id')
        slug_by_seller1  =  request.POST.get('slug_by_seller1')
         
        Category  = request.POST.get('Category') 
        Sub_Category  = request.POST.get('Sub_Category') 
        Type  = request.POST.get('Type') 
        Brand  = request.POST.get('Brand') 
        MRP  = request.POST.get('MRP') 
        Pincode_pro  = request.POST.get('Pincode_pro') 
        Seller_SKU  = request.POST.get('Seller_SKU') 
        Pincode_pro  = request.POST.get('Pincode_pro') 
        Produt_tax_code  = request.POST.get('Produt_tax_code') 
        Shipping_Mode  = request.POST.get('Shipping_Mode') 
        # print(Category)
    
        if check1 == 'True' :
            



            print(check3,check4,check5,check6,check7,check8,check9,check10)
            Category1 = CATEGORY.objects.get(id = Category)
            Sub_Category1 = SUB_CATEGORY.objects.get(id = Sub_Category)
            Type1 = SUB_CATEGORY_Type.objects.get(id = Type)
            Shipping_Mode1 = SHIPPING_MODE.objects.get(id = Shipping_Mode)
            seller1 = SellerAccount.objects.get(id = seller_id)
            # slug_by_seller = Item_by_seller.get(id=slug_by_seller1) I
            Item.objects.get_or_create(
            seller=seller1,
            seller_username=seller,
            title=title_by_seller,
            Category=Category1,
            Sub_Category=Sub_Category1,
            Type=Type1,
            Brand=Brand,
            MRP=MRP,
            Seller_SKU=Seller_SKU,
            Pincode_pro=Pincode_pro,
            Produt_tax_code=Produt_tax_code,
            Shipping_Mode=Shipping_Mode1,
            price=price_by_seller,
            discount_price=discount_price_by_seller,
            slug=slug_by_seller11,
            description=description_by_seller,
            image=image_by_seller ,
            
                )
        
            ABC = Item_by_seller.objects.get(id = slug_by_seller1)
            ABC.delete()
        
        
            messages.success(request, ' Submition Successfull')
            return redirect(reverse('ecom_home:list_of_pro'))
    return render(request, 'ADMIN/review_seller_product.html', data )    

@login_required
def be_seller(request):
    seller = user=request.user
    seller1 = user=request.user.id
    # print(seller1)
    if SellerAccount.objects.filter(user=seller).exists():
        messages.warning(request,'seller already exists')
        return redirect('/dashboard')
    elif SellerAccount_requested.objects.filter(user=seller).exists():
        messages.warning(request,"account is panding")
        
        return redirect('/dashboard' )
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
            return redirect('/dashboard' )


            print(seller)
    # print(name)
     
    return render(request, 'sellers_index.html')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def be_seller_approve(request):
    seller_ac =  SellerAccount_requested.objects.all()
    
    data = {'seller_ac' : seller_ac }
    if request.method == 'POST':
        # check1 =  request.POST.get('approve')
        # check2 =  request.POST.get('approve1')
        check1 =  request.POST.get('AB')
        check2 =  request.POST.get('AID')
        check3 =  request.POST.get('BID')
        print(check2)
        seller2 = User.objects.get(id = check2)
        seller3 = SellerAccount_requested.objects.get(id = check3)
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

def product_listing(request):

    return render(request, 'PRODUCT_LISTING\product_listing.html')  

def navbar(request):
    usr1 = SellerAccount.objects.get(user=request.user)
    data = ORDERS.objects.filter(seller = usr1 , order_received = False  )
    data1 = data.count()

    return render(request, 'ORDERS\navbar.html', {'data1':data1})    

def Orders(request):
    # usr = request.user
    usr1 = SellerAccount.objects.get(user=request.user)
    # for new item count
    data = ORDERS.objects.filter(seller = usr1 , order_received = False  )
    data1 = data.count()
    # for new item count
    print(usr1) 
    
    data = ORDERS.objects.filter(seller = usr1 , order_received = True )
    # for all order
    data2 = data.count()
    # for all order
    # print(OrderItem.seller)
    if request.method == 'POST':
        ID = request.POST.get('ID')
        order_status = ORDERS.objects.get(id=ID)
        order_cancelled = request.POST.get('order_cancelled')
        order_dispatched = request.POST.get('order_dispatched')
        order_status.order_cancelled = order_cancelled
        order_status.order_dispatched = order_dispatched
        order_status.save()
        

    print(data)
    return render(request, 'ORDERS\Orders.html', {'data':data , 'data1':data1 , 'data2':data2})   



def Orders_details(request):

    return render(request, 'ORDERS\Orders_details.html')    
def New_Orders(request):
    usr1 = SellerAccount.objects.get(user=request.user)
    # for all order
    data = ORDERS.objects.filter(seller = usr1 , order_received = True )
    data2 = data.count()
    # for all order
    
    data = ORDERS.objects.filter(seller = usr1 , order_received = False  )
    data1 = data.count()
    
    # print(data1) 
    if request.method == "POST" : 
        ID = request.POST.get('ID')
        order_received = request.POST.get('order_received')
        order_received1 = ORDERS.objects.get(id=ID)
        order_received1.order_received = order_received
        order_received1.save()
        messages.success(request, 'order_received')
        print(order_received)

    return render(request, 'ORDERS\\New_Orders.html' ,{'data':data , 'data1' : data1 , 'data2':data2} )    
def New_Orders_details(request):

    return render(request, 'ORDERS\\New_Orders_details.html')    
   
def Shipped(request):

    return render(request, 'ORDERS\Shipped.html')    
def Shipped_details(request):

    return render(request, 'ORDERS\Shipped_details.html')    
def Pending_Orders(request):

    return render(request, 'ORDERS\Pending_Orders.html')    
def Pending_Orders_details(request):

    return render(request, 'ORDERS\Pending_Orders_details.html')    
def Cancelled(request):

    return render(request, 'ORDERS\Cancelled.html')    
def Cancelled_details(request):

    return render(request, 'ORDERS\Cancelled_details.html')    
def Return(request):

    return render(request, 'ORDERS\Return.html')    
def Return_details(request):

    return render(request, 'ORDERS\Return_details.html')    


def draft(request):
    seller1 = user = request.user
    seller_un =  SellerAccount.objects.get(user__username=request.user)
    seller_item = Item_by_seller.objects.filter(seller=seller_un)        
    data = {'seller_item' : seller_item }
    return render(request, 'PRODUCT_LISTING/draft.html', data )       
# class draft(ListView):
#     model = Item_by_seller
#     # model = Item
    
    # template_name = "draft.html"



def draft_detail(request , slug_by_seller):

    seller_item = Item_by_seller.objects.get(slug_by_seller=slug_by_seller)
    object_list4 = SHIPPING_MODE.objects.all()
    data = {'object' : seller_item , 'object_list4': object_list4 }
    if request.method == 'POST':
        seller = SellerAccount.objects.get(user__username=request.user)

        seller_item_ID  = request.POST.get('seller_item_ID')
        title_by_seller  = request.POST.get('title_by_seller')
        Category1  = request.POST.get('Category') 
        Sub_Category1  = request.POST.get('Sub_Category') 
        Type1  = request.POST.get('Type') 
        Category = CATEGORY.objects.get(id = Category1)
        Sub_Category = SUB_CATEGORY.objects.get(id = Sub_Category1)
        Type = SUB_CATEGORY_Type.objects.get(id = Type1)
        price_by_seller1  = request.POST.get('price_by_seller')
        price_by_seller = float(price_by_seller1)
        discount_price_by_seller  = request.POST.get('discount_price_by_seller')
        discount_price_by_seller = float(discount_price_by_seller)
        # slug_by_seller  = request.POST.get('slug_by_seller')
        description_by_seller  = request.POST.get('description_by_seller')
        image_by_seller  = request.POST.get('image_by_seller')
        Brand = request.POST.get('Brand')
        MRP = request.POST.get('MRP')
        Pincode_pro = request.POST.get('Pincode_pro')
        Seller_SKU = request.POST.get('Seller_SKU')
        Produt_tax_code = request.POST.get('Produt_tax_code')
        Shipping_Mode1 = request.POST.get('Shipping_Mode')
        Shipping_Mode = SHIPPING_MODE.objects.get(id = Shipping_Mode1)
        
        Update_item = Item_by_seller.objects.get(id =seller_item_ID )
        # seller_product_post = Update_item(title_by_seller= title_by_seller, Category= Category , Sub_Category = Sub_Category ,Type=Type,  Brand= Brand, MRP=MRP,  price_by_seller= price_by_seller,Pincode_pro=Pincode_pro, Shipping_Mode=Shipping_Mode  ,discount_price_by_seller=discount_price_by_seller, Seller_SKU=Seller_SKU, Produt_tax_code=Produt_tax_code, slug_by_seller=slug_by_seller, description_by_seller=description_by_seller,image_by_seller=image_by_seller,seller=seller)
        # Update_item.title_by_seller = title_by_seller
        Update_item.Category= Category 
        Update_item.Sub_Category = Sub_Category
        Update_item.Type=Type
        Update_item.Brand= Brand
        Update_item.MRP=MRP
        Update_item.price_by_seller= price_by_seller
        Update_item.Pincode_pro=Pincode_pro
        Update_item.Shipping_Mode=Shipping_Mode 
        Update_item.discount_price_by_seller=discount_price_by_seller
        Update_item.Seller_SKU=Seller_SKU
        Update_item.Produt_tax_code=Produt_tax_code
        # Update_item.slug_by_seller=slug_by_seller
        Update_item.description_by_seller=description_by_seller
        Update_item.image_by_seller=image_by_seller
        
        Update_item.save()
        # messages.success(request, ' Submition Successfull')
        return redirect('/draft' )
    return render(request , 'PRODUCT_LISTING/draft_detail.html' ,data)
def pending(request):
    seller1 = user = request.user
    seller_un =  SellerAccount.objects.get(user__username=request.user)
    
    
    seller_item = Item_by_seller.objects.filter(seller=seller_un)
    data = {'seller_item' : seller_item }
    
            
    return render(request, 'PRODUCT_LISTING/pending.html', data )       

def approved(request):
    seller1 = user = request.user
    seller_un =  SellerAccount.objects.get(user__username=request.user)
    
    item = Item.objects.filter(seller=seller_un)
    data = {'item' : item , 'seller_un': seller_un}   
     
    if request.method == 'POST':
        item_ID = request.POST.get('I')
        stock = request.POST.get('stock')
        T = Item.objects.get(id=item_ID)
        T.stock = stock
        T.save()
        # print(item_ID)
        messages.success(request, 'Stock status changed')
        return redirect('/approved' )


    return render(request, 'PRODUCT_LISTING/approved.html', data )  
def Inventory(request):
    seller1 = user = request.user
    seller_un =  SellerAccount.objects.get(user__username=request.user)
    
    item = Item.objects.filter(seller=seller_un)
    data = {'item' : item , 'seller_un': seller_un}
        
    return render(request, 'INVENTORY/Inventory.html' , data)
def Inventory_search(request):
    seller_un =  SellerAccount.objects.get(user__username=request.user)
    
    if request.method == 'POST':
        qry = request.POST.get('qry')
        if Item.objects.filter(seller = seller_un, slug = qry ).exists():
            data =  Item.objects.filter(seller = seller_un, slug = qry)
            context = {'data' : data }
            print(data)
            return render(request, 'INVENTORY/Inventory_search.html' , context)
        else :
            data2 = 'Product Id Not Found' 
            context = {'data2' : data2 }   
            return render(request, 'INVENTORY/Inventory_search.html' , context)
    return render(request, 'INVENTORY/Inventory_search.html' )

def calculater(request):
    data = cal_cat.objects.all()
    # print(data)



    return render(request, 'calculater.html', {'data':data})     
@login_required
@user_passes_test(lambda u: u.is_superuser)    
def adminn(request):
    
    return render(request, 'ADMIN/adminn.html')     
@login_required
def update_profile(request):
    seller1 = SellerAccount.objects.get(user__username=request.user)
    ID = seller_address.objects.filter(seller=seller1)

    # print(seller1)
    # T = seller_address.objects.get(id=ID)
    if seller_address.objects.filter(seller=seller1).exists():
        # pass
        if request.method == 'POST':
            Buisiness_Name  = request.POST.get('Buisiness_Name')
            GSTN  = request.POST.get('GSTN')
            Pancard_Number  = request.POST.get('Pancard_Number')
            Pancard_Picture  = request.POST.get('Pancard_Picture')
            Owner_Name  = request.POST.get('Owner_Name')
            Address1  = request.POST.get('Address1')
            City  = request.POST.get('City')
            State  = request.POST.get('State')
            Zip  = request.POST.get('Zip')
            Address2  = request.POST.get('Address2')
            City2  = request.POST.get('City2')
            State2  = request.POST.get('State2')
            Zip2  = request.POST.get('Zip2')
            Addharcard_Number  = request.POST.get('Addharcard_Number')
            Addharcard_Picture  = request.POST.get('Addharcard_Picture') 
            
            A  = request.POST.get('I')
            # print(A)
            T = seller_address.objects.get(id=A)
            T.Buisiness_Name = Buisiness_Name
            T.GSTN = GSTN
            T.Pancard_Number = Pancard_Number
            T.Pancard_Picture = Pancard_Picture
            T.Owner_Name = Owner_Name
            T.Address1 = Address1
            T.City = City
            T.Zip =Zip
            T.Address2 =Address2
            T.State=State
            T.City2 =City2
            T.State2 =State2
            T.Zip2 =Zip2
            T.Addharcard_Number = Addharcard_Number
            T.Addharcard_Picture = Addharcard_Picture
            T.save()
            return redirect('/update_profile' )
    else :
        seller1 = SellerAccount.objects.get(user__username=request.user)
        if request.method == 'POST':
            # seller  = request.POST.get('seller')
            Buisiness_Name  = request.POST.get('Buisiness_Name')
            GSTN  = request.POST.get('GSTN')
            Pancard_Number  = request.POST.get('Pancard_Number')
            Pancard_Picture  = request.POST.get('Pancard_Picture')
            Owner_Name  = request.POST.get('Owner_Name')
            Address1  = request.POST.get('Address1')
            City  = request.POST.get('City')
            State  = request.POST.get('State')
            Zip  = request.POST.get('Zip')
            Address2  = request.POST.get('Address2')
            City2  = request.POST.get('City2')
            State2  = request.POST.get('State2')
            Zip2  = request.POST.get('Zip2')
            Addharcard_Number  = request.POST.get('Addharcard_Number')
            Addharcard_Picture  = request.POST.get('Addharcard_Picture')
            
            update_profile = seller_address(seller= seller1,  Buisiness_Name = Buisiness_Name, GSTN=GSTN, Pancard_Number=Pancard_Number, Pancard_Picture=Pancard_Picture,Owner_Name=Owner_Name,Address1=Address1, City =City, Zip =Zip, Address2 =Address2,State=State, City2 =City2, State2 =State2, Zip2 =Zip2, Addharcard_Number =Addharcard_Number, Addharcard_Picture = Addharcard_Picture)
            update_profile.save()
            return redirect('/update_profile' )
    return render(request, 'account/update_profile.html', {'ID':ID})     


def list_of_pro(request  ):
    
    seller_item = Item_by_seller.objects.all()
    data = {'seller_item' : seller_item }
    

            
    return render(request, 'ADMIN/list_seller_product.html', data )       
