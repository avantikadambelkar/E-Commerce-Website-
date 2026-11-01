from django.urls import path
from . import views

urlpatterns = [
    # Storefront
    path('', views.home_view, name='home'),
    path('shop/', views.product_list_view, name='shop'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),

    # Cart (CRUD)
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity_view, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/apply-coupon/', views.apply_coupon_view, name='apply_coupon'),
    path('cart/remove-coupon/', views.remove_coupon_view, name='remove_coupon'),

    # Wishlist (CRUD)
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),

    # Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/place-order/', views.place_order_view, name='place_order'),
    path('order/confirmation/<str:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('order/track/', views.order_tracking_view, name='order_tracking'),
    path('my-orders/', views.my_orders_view, name='my_orders'),

    # Custom Storefront CRUD Manager Dashboard
    path('manage/products/', views.manage_products_view, name='manage_products'),
    path('manage/products/new/', views.product_create_view, name='product_create'),
    path('manage/products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('manage/products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
