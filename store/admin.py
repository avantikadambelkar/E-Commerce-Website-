from django.contrib import admin
from .models import (
    Category, Product, ProductImage, ProductVariant,
    Cart, CartItem, Wishlist, Coupon, Order, OrderItem, Review
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'display_order')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'original_price', 'stock_count', 'badge', 'is_featured', 'is_trending', 'created_at')
    list_filter = ('category', 'is_featured', 'is_trending', 'is_new_arrival', 'brand')
    list_editable = ('price', 'stock_count', 'is_featured', 'is_trending')
    search_fields = ('name', 'brand', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'variant_info', 'price', 'quantity', 'total_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'full_name', 'email', 'phone', 'total_amount', 'payment_method', 'payment_status', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'full_name', 'email', 'phone', 'tracking_number')
    list_editable = ('order_status', 'payment_status')
    inlines = [OrderItemInline]

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'flat_discount', 'min_purchase', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('code',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'reviewer_name', 'rating', 'verified_purchase', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('reviewer_name', 'product__name', 'comment')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
