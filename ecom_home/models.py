from django.conf import settings
from django.db import models
from django.shortcuts import reverse

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
    title = models.CharField(max_length=100)
    price = models.FloatField()
    # CATEGORY = models.CharField( 
    #     max_length = 20, 
    #     choices = CHOICES, 
    #     default = 'All'
    #     )
    discount_price = models.FloatField(blank=True, null=True)
   
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to = 'static' , storage=None )

    def __str__(self):
        return self.slug

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
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    # country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
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
    price_by_seller = models.FloatField()
    discount_price_by_seller = models.FloatField(blank=True, null=True)
    Category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE , null=True)
    
    slug_by_seller = models.SlugField()
    description_by_seller = models.TextField()
    image_by_seller = models.ImageField( upload_to = 'static/media')

    def __str__(self):
        return self.title_by_seller

    # def get_absolute_url(self):
    #     return reverse("ecom_home:product", kwargs={
    #         'slug_by_seller': self.slug_by_seller
    #     })
class cal_cat(models.Model):
    category_product = models.CharField(max_length=100)
    Category_price = models.FloatField()
