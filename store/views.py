from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q, Count, Avg, Sum
from decimal import Decimal
import json

from .models import (
    Category, Product, ProductImage, ProductVariant,
    Cart, CartItem, Wishlist, Coupon, Order, OrderItem, Review
)
from .forms import ProductForm, ReviewForm, CheckoutForm, CouponApplyForm, RegisterForm
from .context_processors import get_or_create_cart, get_or_create_wishlist


# ==========================================
# PUBLIC STOREFRONT VIEWS
# ==========================================

def home_view(request):
    featured_categories = Category.objects.filter(is_featured=True)[:6]
    trending_products = Product.objects.filter(is_trending=True).select_related('category')[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True).select_related('category')[:8]
    featured_products = Product.objects.filter(is_featured=True).select_related('category')[:4]
    
    context = {
        'featured_categories': featured_categories,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'featured_products': featured_products,
    }
    return render(request, 'store/home.html', context)


def product_list_view(request):
    products = Product.objects.all().select_related('category')
    
    # Filter by category slug
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        
    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        )
        
    # Price filtering in INR
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass
            
    # Stock status filter
    in_stock_only = request.GET.get('in_stock')
    if in_stock_only == '1':
        products = products.filter(stock_count__gt=0)
        
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'popular':
        products = products.order_by('-rating_count')
    else:
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(prod_count=Count('products'))

    context = {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'current_category': category_slug,
        'search_query': query,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'current_sort': sort_by,
        'total_count': paginator.count,
    }
    return render(request, 'store/shop.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all()
    review_form = ReviewForm()

    # Handle Review Submission
    if request.method == 'POST' and 'submit_review' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            if request.user.is_authenticated:
                new_review.user = request.user
                if not new_review.reviewer_name:
                    new_review.reviewer_name = request.user.get_full_name() or request.user.username
            new_review.save()
            
            # Recalculate average rating
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
            product.rating = round(Decimal(avg_rating), 1)
            product.rating_count = reviews.count()
            product.save()

            messages.success(request, "Thank you! Your verified review has been published.")
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'store/product_detail.html', context)


# ==========================================
# CART & CHECKOUT VIEWS (CRUD)
# ==========================================

def cart_view(request):
    cart = get_or_create_cart(request)
    coupon_form = CouponApplyForm()
    
    # Check if coupon is still valid
    if cart.coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=cart.coupon_code, is_active=True)
            cart.coupon_discount = coupon.calculate_discount(cart.subtotal)
            cart.save()
        except Coupon.DoesNotExist:
            cart.coupon_code = None
            cart.coupon_discount = Decimal('0.00')
            cart.save()

    context = {
        'cart': cart,
        'coupon_form': coupon_form,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    # If coupon applied, recalculate
    if cart.coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=cart.coupon_code, is_active=True)
            cart.coupon_discount = coupon.calculate_discount(cart.subtotal)
            cart.save()
        except Coupon.DoesNotExist:
            pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to bag.",
            'cart_count': cart.total_items,
            'cart_subtotal': float(cart.subtotal),
        })

    messages.success(request, f"Added '{product.name}' to your luxury shopping bag.")
    return redirect('cart')


def update_cart_quantity_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)

    # Ensure cart item belongs to active cart
    if cart_item.cart != cart:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'set':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            cart_item.quantity = qty
            cart_item.save()
        else:
            cart_item.delete()

    # Recalculate coupon
    if cart.coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=cart.coupon_code, is_active=True)
            cart.coupon_discount = coupon.calculate_discount(cart.subtotal)
            cart.save()
        except Coupon.DoesNotExist:
            pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'item_total': float(cart_item.total_price) if cart_item.id else 0,
            'cart_subtotal': float(cart.subtotal),
            'cart_tax': float(cart.tax),
            'cart_shipping': float(cart.shipping_fee),
            'cart_discount': float(cart.coupon_discount),
            'cart_grand_total': float(cart.grand_total),
        })

    return redirect('cart')


def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    if cart_item.cart == cart:
        product_name = cart_item.product.name
        cart_item.delete()
        
        if cart.coupon_code:
            try:
                coupon = Coupon.objects.get(code__iexact=cart.coupon_code, is_active=True)
                cart.coupon_discount = coupon.calculate_discount(cart.subtotal)
                cart.save()
            except Coupon.DoesNotExist:
                pass
                
        messages.info(request, f"Removed '{product_name}' from bag.")

    return redirect('cart')


def apply_coupon_view(request):
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip().upper()
            cart = get_or_create_cart(request)
            try:
                coupon = Coupon.objects.get(code__iexact=code, is_active=True)
                if cart.subtotal < coupon.min_purchase:
                    messages.error(request, f"Coupon '{code}' requires a minimum order of ₹{coupon.min_purchase}.")
                else:
                    discount = coupon.calculate_discount(cart.subtotal)
                    cart.coupon_code = coupon.code
                    cart.coupon_discount = discount
                    cart.save()
                    messages.success(request, f"Coupon '{coupon.code}' applied! You saved ₹{discount}.")
            except Coupon.DoesNotExist:
                messages.error(request, f"Invalid promo code '{code}'. Try code 'AURA10' or 'FESTIVE500'.")
    return redirect('cart')


def remove_coupon_view(request):
    cart = get_or_create_cart(request)
    cart.coupon_code = None
    cart.coupon_discount = Decimal('0.00')
    cart.save()
    messages.info(request, "Promo code removed.")
    return redirect('cart')


# ==========================================
# WISHLIST (CRUD)
# ==========================================

def wishlist_view(request):
    wishlist = get_or_create_wishlist(request)
    products = wishlist.products.all()
    return render(request, 'store/wishlist.html', {'products': products})


def toggle_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        in_wishlist = False
        msg = f"Removed '{product.name}' from your wishlist."
    else:
        wishlist.products.add(product)
        in_wishlist = True
        msg = f"Saved '{product.name}' to your wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'message': msg,
            'wishlist_count': wishlist.products.count()
        })

    messages.info(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ==========================================
# CHECKOUT & ORDERS
# ==========================================

def checkout_view(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.warning(request, "Your shopping bag is empty. Explore our collection before checking out.")
        return redirect('shop')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)


def place_order_view(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.error(request, "Your bag is empty.")
        return redirect('shop')

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        context = {'cart': cart, 'form': form}
        return render(request, 'store/checkout.html', context)

    # Create Order
    data = form.cleaned_data
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        address_line1=data['address_line1'],
        address_line2=data['address_line2'],
        city=data['city'],
        state=data['state'],
        pincode=data['pincode'],
        subtotal=cart.subtotal,
        tax=cart.tax,
        shipping_fee=cart.shipping_fee,
        discount=cart.coupon_discount,
        total_amount=cart.grand_total,
        payment_method=data['payment_method'],
        payment_status='Paid' if data['payment_method'] != 'cod' else 'Pending on Delivery',
        order_status='Confirmed',
        estimated_delivery="Within 3-4 Business Days"
    )

    # Create OrderItems & decrement stock
    for item in cart.items.all():
        variant_desc = f"{item.variant.name}: {item.variant.value}" if item.variant else ""
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_image=item.product.main_image,
            variant_info=variant_desc,
            price=item.unit_price,
            quantity=item.quantity,
            total_price=item.total_price
        )
        # Deduct stock safely
        if item.product.stock_count >= item.quantity:
            item.product.stock_count -= item.quantity
            item.product.save()

    # Clear Cart
    cart.items.all().delete()
    cart.coupon_code = None
    cart.coupon_discount = Decimal('0.00')
    cart.save()

    messages.success(request, f"Order #{order.order_id} placed successfully! A confirmation SMS and email have been initiated.")
    return redirect('order_confirmation', order_id=order.order_id)


def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})


def order_tracking_view(request):
    order = None
    searched = False
    query = request.GET.get('order_id', '').strip()

    if query:
        searched = True
        try:
            order = Order.objects.filter(
                Q(order_id__iexact=query) | Q(tracking_number__iexact=query)
            ).first()
        except Exception:
            order = None

    return render(request, 'store/order_tracking.html', {'order': order, 'searched': searched, 'query': query})


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/my_orders.html', {'orders': orders})


# ==========================================
# CUSTOM STORE MANAGEMENT / CRUD DASHBOARD
# ==========================================

def manage_products_view(request):
    """Integrated Store Manager dashboard for viewing, creating, updating, and deleting catalog products."""
    products = Product.objects.all().select_related('category')
    
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(category__name__icontains=q))

    # Stats
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock_count__lt=10).count()
    total_orders = Order.objects.count()
    revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'total_products': total_products,
        'low_stock': low_stock,
        'total_orders': total_orders,
        'revenue': revenue,
        'search_query': q,
    }
    return render(request, 'store/manage_products.html', context)


def product_create_view(request):
    """CRUD: Create new Product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('manage_products')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'title': 'Create New Luxury Item'})


def product_edit_view(request, pk):
    """CRUD: Update Product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html', {'form': form, 'title': f"Edit '{product.name}'", 'product': product})


def product_delete_view(request, pk):
    """CRUD: Delete Product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' has been deleted from catalog.")
        return redirect('manage_products')

    return render(request, 'store/product_confirm_delete.html', {'product': product})


# ==========================================
# AUTHENTICATION
# ==========================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            login(request, user)
            messages.success(request, f"Welcome to AURA, {user.first_name or user.username}! Enjoy exclusive member drops.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password credentials.")

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely signed out. We hope to see you soon.")
    return redirect('home')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)[:5]
    wishlist = get_or_create_wishlist(request)
    wishlist_items = wishlist.products.all()[:4]
    
    return render(request, 'store/profile.html', {
        'orders': orders,
        'wishlist_items': wishlist_items,
    })
