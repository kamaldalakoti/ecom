from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from datetime import datetime 
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class SellerAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , default=None, null=True)
    name == user
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="manager_sellers",
        blank=True
    )
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        # return str(self.user.username)
        return str(self.user)
    def __unicode__(self):
        return self.name
class SellerAccount_requested(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , default=None, null=True)
    # name == user
    # managers = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name="manager_sellers",
    #     blank=True
    # )
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        # return str(self.user.username)
        return str(self.user)
    def __unicode__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("products:vendor_detail", kwargs={"vendor_name": self.user.username})

class CATEGORY(models.Model):
    Category = models.CharField(max_length=30 ,null=True )
    def __str__(self):
        return self.Category
    def get_cat(self):
        return reverse("ecom_home:Sub_Category", kwargs={
            'Category': self.id
        })  
class SUB_CATEGORY(models.Model):
    Category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE)
    Sub_Category = models.CharField(max_length=30 )
    def __str__(self):
        return self.Sub_Category
    def get_sub_cat(self):
        return reverse("ecom_home:Type", kwargs={
            'Sub_Category': self.id
        }) 
      
class SUB_CATEGORY_Type(models.Model):
    Category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE)
    Sub_Category =models.ForeignKey(SUB_CATEGORY, on_delete=models.CASCADE)
    Type = models.CharField(max_length=30 )
    def __str__(self):
        return self.Type
    def get_sub_cat_type(self):
        return reverse("ecom_home:seller_product_post", kwargs={
            'Type': self.id
        })   
class SHIPPING_MODE(models.Model):
    Shipping_Mode = models.CharField(max_length=50, default=None)
    def __unicode__(self):
        return self.Shipping_Mode
    def __str__(self):
        return self.Shipping_Mode    
class Item(models.Model):
    # CHOICES = (
    # ("All","All"),
    # ("Clothing", "Clothing"),
    # ("Electronics", "Electronics"),
    # ("Books", "Books"),
    # ("Sports", "Sports")

    seller_username = models.CharField(max_length=100 , null=True, )
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE, null=True  )
    # seller = seller_username
    Category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE , null=True)
    Sub_Category = models.ForeignKey(SUB_CATEGORY, on_delete=models.CASCADE , null=True)
    Type = models.ForeignKey(SUB_CATEGORY_Type, on_delete=models.CASCADE , null=True)
    stock = models.BooleanField(default=True , null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    # CATEGORY = models.CharField( 
    #     max_length = 20, 
    #     choices = CHOICES, 
    #     default = 'All'
    #     )
    Brand = models.CharField(max_length=50, blank=True,null=True)
    Produt_tax_code = models.CharField(max_length=50 ,blank=True,null=True)
    Pincode_pro  = models.CharField(max_length=50,blank=True,null=True)
    Shipping_Mode = models.ForeignKey(SHIPPING_MODE,on_delete=models.CASCADE , null=True)
    MRP = models.FloatField(default=10)
    Shipping_Mode = models.ForeignKey(SHIPPING_MODE,on_delete=models.CASCADE , null=True)
    Seller_SKU = models.CharField(max_length=50,blank=True,null=True)
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to = 'static')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecom_home:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecom_home:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("ecom_home:remove-from-cart", kwargs={
            'slug': self.slug
        })
   

class Display2(models.Model):
    slug = models.ForeignKey(Item, on_delete=models.CASCADE)
    def __str__(self):
        return self.slug

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE, null=True  )                         
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
# ADDRESS_CHOICES = (
#     ('B', 'Billing'),
#     ('S', 'Shipping'),
# )        
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city  = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    # country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
class ORDERS(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE , null=True )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)    
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField( default=1)
    street_address = models.CharField(max_length=50 , null=True )
    apartment_address = models.CharField(max_length=50, null=True )
    landmark = models.CharField(max_length=50, null=True )
    city = models.CharField(max_length=50, null=True )
    state = models.CharField(max_length=50, null=True )
    country = models.CharField(max_length=50 ,null=True )
    zip_code = models.CharField(max_length=50 ,null=True )
    order_received = models.BooleanField(default=False )
    order_cancelled = models.BooleanField(default=False ,null = True  )
    order_dispatched = models.BooleanField(default=False , null = True )
    # street_address = models.ForeignKey(Address, on_delete=models.CASCADE , null=True )
    def __str__(self):
        return self.item.slug

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # Ordered = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total



class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE , null=True)
    user_name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_phone_no = models.CharField(max_length=30 , null=True)
    # user_password = models.CharField(max_length=30)
    user_address = models.CharField(max_length=300)
    user_pincode = models.IntegerField()
   


class signup2(models.Model):
    user_name1 = models.CharField(max_length=30)
    user_email1 = models.CharField(max_length=30)
    user_phone_no1 = models.CharField(max_length=30)
    user_password1 = models.CharField(max_length=30)
    user_address1 = models.CharField(max_length=300)
    user_pincode1 = models.CharField(max_length=10)


class Item_by_seller(models.Model):
    # seller_username = models.CharField(max_length=100 , null=True, default=settings.AUTH_USER_MODEL )
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE , null=True )
    # 
    title_by_seller = models.CharField(max_length=100)
    price_by_seller = models.FloatField(default=0, null=True)
    discount_price_by_seller = models.FloatField(blank=True, default=0, null=True)
    Category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE , null=True)
    Sub_Category = models.ForeignKey(SUB_CATEGORY, on_delete=models.CASCADE , null=True)
    Type = models.ForeignKey(SUB_CATEGORY_Type, on_delete=models.CASCADE , null=True)
    Produt_tax_code = models.CharField(max_length=50 ,blank=True,null=True)
    Brand = models.CharField(max_length=50, blank=True,null=True)
    Pincode_pro  = models.CharField(max_length=50,blank=True,null=True)
    
    MRP = models.FloatField(default=10, null=True)
    Shipping_Mode = models.ForeignKey(SHIPPING_MODE,on_delete=models.CASCADE , default='ALMORIANS', null=True)
    Seller_SKU = models.CharField(max_length=50,blank=True,null=True)
    
    
    slug_by_seller = models.SlugField()
    description_by_seller = models.TextField( null=True)
    image_by_seller = models.ImageField( upload_to = 'static' ,null=True)

    def __str__(self):
        return self.title_by_seller

    def get_absolute1_url(self):
        return reverse("ecom_home:draft_detail", kwargs={
            'slug_by_seller': self.slug_by_seller
        })
    def get_absolute12_url(self):
        return reverse("ecom_home:review_seller_product", kwargs={
            'slug_by_seller': self.slug_by_seller
        })
class cal_cat(models.Model):
    category_product = models.CharField(max_length=100)
    Category_price = models.FloatField()
    def __unicode__(self):
        return self.name
class seller_address(models.Model):
    seller = models.ForeignKey(SellerAccount ,on_delete=models.CASCADE , null=True )
    Buisiness_Name = models.CharField(max_length=100 ,null=True)
    GSTN = models.CharField(max_length=100,null=True)
    Pancard_Number = models.CharField(max_length=100,null=True)
    Pancard_Picture =models.ImageField( upload_to = 'static',null=True)
    Owner_Name = models.CharField(max_length=100,null=True)
    Address1 = models.CharField(max_length=100,null=True)
    City = models.CharField(max_length=100,null=True)
    State = models.CharField(max_length=100,null=True)
    Zip = models.CharField(max_length=100,null=True)
    Address2 = models.CharField(max_length=100,null=True)
    City2 = models.CharField(max_length=100,null=True)
    State2 = models.CharField(max_length=100,null=True)
    Zip2 = models.CharField(max_length=100,null=True)
    Addharcard_Number = models.CharField(max_length=100,null=True)
    Addharcard_Picture = models.ImageField( upload_to = 'static',null=True)
    
    # def __unicode__(self):
    #     return self.seller
    def __str__(self):
        return self.Owner_Name
