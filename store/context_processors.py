from .models import Cart, Wishlist, Category

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

def get_or_create_wishlist(request):
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        wishlist, _ = Wishlist.objects.get_or_create(session_key=session_key)
    return wishlist

def store_context(request):
    try:
        cart = get_or_create_cart(request)
        cart_count = cart.total_items
        cart_subtotal = cart.subtotal
    except Exception:
        cart_count = 0
        cart_subtotal = 0

    try:
        wishlist = get_or_create_wishlist(request)
        wishlist_count = wishlist.products.count()
        wishlist_product_ids = list(wishlist.products.values_list('id', flat=True))
    except Exception:
        wishlist_count = 0
        wishlist_product_ids = []

    try:
        categories = Category.objects.all()[:8]
    except Exception:
        categories = []

    return {
        'cart_count': cart_count,
        'cart_subtotal': cart_subtotal,
        'wishlist_count': wishlist_count,
        'wishlist_product_ids': wishlist_product_ids,
        'nav_categories': categories,
        'CURRENCY_SYMBOL': '₹',
    }
