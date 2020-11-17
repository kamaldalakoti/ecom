from django.contrib import admin
from django.urls import path
from ecom_home import views
from .views import*

app_name = 'ecom_home'

urlpatterns = [

    # path('',views.indexView.as_view(),name='home'),
    # path('Home',views.index,name='home'),
    # path('Home',indexView.as_view(),name='home'),
    # path('SignUp',views.signup1,name='signup'),
    # path('product/<slug>/',productsDetailView.as_view(),name='product'),
    path('sell_with_us',views.sell_with_us,name='sell_with_us'),
    path('calculater',views.calculater,name='calculater'),
    path('be_seller_approve/', views.be_seller_approve, name='be_seller_approve'),
    path('login',views.login,name='login'),
    # path('cart',views.cart,name='cart'),
    path('dashboard/', SellerDashboard.as_view(), name='dashboard'),

    path('profile/',views.profile,name='profile'),
    path('seller_account/',views.be_seller,name='Seller_account'),
    path('review_seller_product/',views.review_seller_product,name='review_seller_product'),
    path('seller_product_post',views.seller_product_post,name='seller_product_post'),
    path('', indexView.as_view(), name='home'),
    path('Home', indexView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    # path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
        name='remove-single-item-from-cart'),
    # path('payment/', PaymentView.as_view(), name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
