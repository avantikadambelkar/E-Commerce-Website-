/**
 * AURA LUXE - Interactive Shopping App Client Script
 * AJAX Cart, Wishlist toggles, Dynamic Price Updates, and Payment toggles
 */

document.addEventListener('DOMContentLoaded', function () {
    // Helper to get CSRF token from cookie or DOM
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        if (!cookieValue) {
            const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfInput) cookieValue = csrfInput.value;
        }
        return cookieValue;
    }

    // Toast Notification Creator
    function showToast(message, type = 'success') {
        let container = document.querySelector('.aura-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'aura-toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = 'aura-toast';
        const icon = type === 'success' ? 'bi-check-circle-fill text-success' : 'bi-info-circle-fill text-warning';
        toast.innerHTML = `
            <i class="bi ${icon} fs-5"></i>
            <div>
                <div class="fw-semibold small">${message}</div>
            </div>
            <button type="button" class="btn-close btn-close-white ms-auto" aria-label="Close" style="font-size: 0.7rem;"></button>
        `;

        toast.querySelector('.btn-close').addEventListener('click', () => toast.remove());
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }

    // Global Wishlist AJAX Toggle
    document.querySelectorAll('.wishlist-toggle-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const productId = this.getAttribute('data-product-id');
            const url = `/wishlist/toggle/${productId}/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    if (data.in_wishlist) {
                        this.classList.add('active');
                        this.querySelector('i').classList.remove('bi-heart');
                        this.querySelector('i').classList.add('bi-heart-fill');
                    } else {
                        this.classList.remove('active');
                        this.querySelector('i').classList.remove('bi-heart-fill');
                        this.querySelector('i').classList.add('bi-heart');
                    }

                    // Update Wishlist Badges
                    document.querySelectorAll('.wishlist-counter-badge').forEach(badge => {
                        badge.textContent = data.wishlist_count;
                        badge.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
                    });

                    showToast(data.message, 'success');
                }
            })
            .catch(err => {
                console.error(err);
            });
        });
    });

    // Quick Add to Cart via AJAX from product cards
    document.querySelectorAll('.ajax-add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const url = `/cart/add/${productId}/`;
            const originalHtml = this.innerHTML;

            this.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Adding...`;
            this.disabled = true;

            const formData = new FormData();
            formData.append('quantity', 1);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                this.innerHTML = `<i class="bi bi-check2"></i> Added`;
                setTimeout(() => {
                    this.innerHTML = originalHtml;
                    this.disabled = false;
                }, 1500);

                if (data.success) {
                    // Update Cart Badges
                    document.querySelectorAll('.cart-counter-badge').forEach(badge => {
                        badge.textContent = data.cart_count;
                        badge.style.display = data.cart_count > 0 ? 'flex' : 'none';
                    });
                    showToast(data.message, 'success');
                }
            })
            .catch(err => {
                console.error(err);
                this.innerHTML = originalHtml;
                this.disabled = false;
            });
        });
    });

    // Cart Quantity Controls (+ / -)
    document.querySelectorAll('.cart-qty-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            const action = this.getAttribute('data-action');
            const row = document.getElementById(`cart-row-${itemId}`);

            const formData = new FormData();
            formData.append('action', action);

            fetch(`/cart/update/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // If item removed (quantity 0)
                    if (data.item_total === 0 && row) {
                        row.remove();
                    } else if (row) {
                        const input = row.querySelector('.cart-qty-input');
                        if (input) {
                            let curr = parseInt(input.value);
                            input.value = action === 'increase' ? curr + 1 : Math.max(1, curr - 1);
                        }
                        const itemTotalElem = row.querySelector('.item-total-price');
                        if (itemTotalElem) {
                            itemTotalElem.textContent = `₹${data.item_total.toLocaleString('en-IN')}`;
                        }
                    }

                    // Update Cart Total Badges and Summary Elements
                    document.querySelectorAll('.cart-counter-badge').forEach(badge => {
                        badge.textContent = data.cart_count;
                        badge.style.display = data.cart_count > 0 ? 'flex' : 'none';
                    });

                    const subtotalElem = document.getElementById('cart-summary-subtotal');
                    if (subtotalElem) subtotalElem.textContent = `₹${data.cart_subtotal.toLocaleString('en-IN')}`;

                    const taxElem = document.getElementById('cart-summary-tax');
                    if (taxElem) taxElem.textContent = `₹${data.cart_tax.toLocaleString('en-IN')}`;

                    const shipElem = document.getElementById('cart-summary-shipping');
                    if (shipElem) {
                        shipElem.textContent = data.cart_shipping === 0 ? 'FREE' : `₹${data.cart_shipping}`;
                    }

                    const grandTotalElem = document.getElementById('cart-summary-grand-total');
                    if (grandTotalElem) grandTotalElem.textContent = `₹${data.cart_grand_total.toLocaleString('en-IN')}`;

                    if (data.cart_count === 0) {
                        location.reload();
                    }
                }
            })
            .catch(err => console.error(err));
        });
    });

    // Checkout Payment Method Interactive Toggle
    const paymentRadios = document.querySelectorAll('input[name="payment_method"]');
    const upiBox = document.getElementById('upi-payment-details');
    const cardBox = document.getElementById('card-payment-details');
    const codBox = document.getElementById('cod-payment-details');

    if (paymentRadios.length > 0) {
        function updatePaymentUI() {
            const selected = document.querySelector('input[name="payment_method"]:checked')?.value;
            if (upiBox) upiBox.style.display = selected === 'upi' ? 'block' : 'none';
            if (cardBox) cardBox.style.display = selected === 'card' ? 'block' : 'none';
            if (codBox) codBox.style.display = selected === 'cod' ? 'block' : 'none';
        }

        paymentRadios.forEach(radio => {
            radio.addEventListener('change', updatePaymentUI);
        });
        updatePaymentUI();
    }
});
