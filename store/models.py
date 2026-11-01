from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import uuid

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True, help_text="Short subtitle for luxury collection")
    image_url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, default='bi-tag', help_text="Bootstrap icon class")
    is_featured = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=275, unique=True, blank=True)
    brand = models.CharField(max_length=100, default='AURA STUDIO')
    short_description = models.CharField(max_length=300, help_text="Punchy 1-2 sentence overview")
    description = models.TextField(help_text="Detailed product storytelling, craft details, specs")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current selling price in INR")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="MRP before discount in INR")
    stock_count = models.IntegerField(default=25)
    badge = models.CharField(max_length=50, blank=True, help_text="E.g., 'EDITOR’S PICK', 'EXCLUSIVE DROP', 'LIMITED RUN'")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.8)
    rating_count = models.IntegerField(default=18)
    image_url = models.URLField(max_length=500, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=True)
    material = models.CharField(max_length=120, blank=True, default='Handcrafted Luxury Blend')
    care_instructions = models.CharField(max_length=200, blank=True, default='Dry clean only or wipe with microfiber cloth')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return int(round(discount))
        return 0

    @property
    def is_in_stock(self):
        return self.stock_count > 0

    @property
    def main_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=800&auto=format&fit=crop"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=50, help_text="e.g. Size, Color, Edition")
    value = models.CharField(max_length=50, help_text="e.g. Small, Medium, Large or Noir Black, Gold")
    additional_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    stock = models.IntegerField(default=15)

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=100, blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} ({self.user.username if self.user else 'Guest'})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def tax(self):
        # 12% GST
        return round(self.subtotal * Decimal('0.12'), 2)

    @property
    def shipping_fee(self):
        if self.subtotal == 0:
            return Decimal('0.00')
        # Complimentary shipping above ₹1,499
        if self.subtotal >= Decimal('1499.00'):
            return Decimal('0.00')
        return Decimal('149.00')

    @property
    def grand_total(self):
        if self.subtotal == 0:
            return Decimal('0.00')
        total = self.subtotal + self.tax + self.shipping_fee - self.coupon_discount
        return max(total, Decimal('0.00'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_at']

    @property
    def unit_price(self):
        base = self.product.price
        if self.variant:
            base += self.variant.additional_price
        return base

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist')
    session_key = models.CharField(max_length=100, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='wishlisted_in')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist ({self.user.username if self.user else self.session_key})"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    flat_discount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    min_purchase = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Coupon {self.code}"

    def calculate_discount(self, subtotal):
        if subtotal < self.min_purchase:
            return Decimal('0.00')
        if self.discount_percentage > 0:
            return round((subtotal * self.discount_percentage) / Decimal('100.00'), 2)
        return min(self.flat_discount, subtotal)


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('upi', 'Instant UPI / QR Code (Google Pay, PhonePe, Paytm, BHIM)'),
        ('card', 'Credit / Debit Card (Visa, Mastercard, RuPay)'),
        ('netbanking', 'Net Banking (All Indian Major Banks)'),
        ('cod', 'Cash on Delivery (₹50 Express Handling)'),
    ]

    STATUS_CHOICES = [
        ('Confirmed', 'Order Placed & Confirmed'),
        ('Processing', 'Packed & Quality Verified'),
        ('Shipped', 'Handed over to Express Courier (BlueDart / Delhivery)'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered Safely'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='upi')
    payment_status = models.CharField(max_length=30, default='Paid')
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Confirmed')
    tracking_number = models.CharField(max_length=100, blank=True)
    estimated_delivery = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"AURA-{uuid.uuid4().hex[:8].upper()}"
        if not self.tracking_number:
            self.tracking_number = f"EXP-IN-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField(max_length=500, blank=True)
    variant_info = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_id}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_name = models.CharField(max_length=100)
    reviewer_city = models.CharField(max_length=100, default='Bengaluru, India')
    rating = models.IntegerField(default=5) # 1 to 5
    title = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} ({self.rating}★) on {self.product.name}"
