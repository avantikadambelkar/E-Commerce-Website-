from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from store.models import Category, Product, Cart, CartItem, Wishlist, Coupon, Order, OrderItem, Review

class AuraEcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Horology",
            slug="horology",
            tagline="Fine watches"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Chronos Watch 40mm",
            slug="chronos-watch-40mm",
            brand="AURA STUDIO",
            short_description="Precision watch",
            description="Detailed watch craftsmanship narrative",
            price=Decimal('15000.00'),
            original_price=Decimal('18000.00'),
            stock_count=10,
            image_url="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9"
        )
        self.coupon = Coupon.objects.create(
            code="AURA10",
            discount_percentage=Decimal('10.00'),
            min_purchase=Decimal('1000.00')
        )
        self.user = User.objects.create_user(username="patron", password="password123", email="patron@example.com")

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chronos Watch 40mm")
        self.assertContains(response, "AURA")

    def test_shop_catalog_and_filtering(self):
        response = self.client.get(reverse('shop') + '?category=horology')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chronos Watch 40mm")

    def test_product_detail_page(self):
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "₹15000")

    def test_cart_crud_operations(self):
        # 1. Add to cart
        add_url = reverse('add_to_cart', kwargs={'product_id': self.product.id})
        response = self.client.post(add_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.total_items, 2)
        self.assertEqual(cart.subtotal, Decimal('30000.00'))

        # 2. Update quantity
        item = cart.items.first()
        update_url = reverse('update_cart_quantity', kwargs={'item_id': item.id})
        self.client.post(update_url, {'action': 'increase'})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

        # 3. Apply coupon
        coupon_url = reverse('apply_coupon')
        self.client.post(coupon_url, {'code': 'AURA10'})
        cart.refresh_from_db()
        self.assertEqual(cart.coupon_code, 'AURA10')
        self.assertTrue(cart.coupon_discount > 0)

        # 4. Remove item
        remove_url = reverse('remove_from_cart', kwargs={'item_id': item.id})
        self.client.get(remove_url)
        self.assertEqual(cart.items.count(), 0)

    def test_wishlist_toggle(self):
        toggle_url = reverse('toggle_wishlist', kwargs={'product_id': self.product.id})
        response = self.client.post(toggle_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['in_wishlist'])

    def test_checkout_and_place_order(self):
        # Add product to cart first
        self.client.post(reverse('add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 1})
        
        # Place order
        order_data = {
            'full_name': 'Vikram Rathore',
            'email': 'vikram@example.com',
            'phone': '+91 98765 43210',
            'address_line1': '104, Regency Palms, Linking Road',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400050',
            'payment_method': 'upi',
        }
        response = self.client.post(reverse('place_order'), order_data)
        self.assertEqual(response.status_code, 302)

        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Vikram Rathore')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.city, 'Mumbai')

    def test_product_crud_management(self):
        # Create product via view
        new_prod_data = {
            'category': self.category.id,
            'name': 'Artisanal Silk Scarf',
            'brand': 'AURA STUDIO',
            'short_description': 'Handloom silk scarf',
            'description': 'Pure mulberry handloom silk narrative description',
            'price': '3499.00',
            'original_price': '4499.00',
            'stock_count': 15,
            'material': '100% Silk',
            'care_instructions': 'Dry clean only',
        }
        response = self.client.post(reverse('product_create'), new_prod_data)
        self.assertEqual(response.status_code, 302)
        created_prod = Product.objects.filter(name='Artisanal Silk Scarf').first()
        self.assertIsNotNone(created_prod)

        # Update product
        edit_url = reverse('product_edit', kwargs={'pk': created_prod.pk})
        new_prod_data['price'] = '3899.00'
        self.client.post(edit_url, new_prod_data)
        created_prod.refresh_from_db()
        self.assertEqual(created_prod.price, Decimal('3899.00'))

        # Delete product
        del_url = reverse('product_delete', kwargs={'pk': created_prod.pk})
        self.client.post(del_url)
        self.assertFalse(Product.objects.filter(name='Artisanal Silk Scarf').exists())
