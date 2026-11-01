from django import forms
from django.contrib.auth.models import User
from .models import Product, Review, Order

INDIAN_STATES = [
    ('', 'Select State / UT'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Delhi', 'Delhi NCR'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'brand', 'short_description', 'description',
            'price', 'original_price', 'stock_count', 'badge',
            'image_url', 'image', 'is_featured', 'is_trending', 'is_new_arrival',
            'material', 'care_instructions'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. Noir Minimalist Chrono Watch'}),
            'brand': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Brand Name (e.g. AURA LUXE)'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Brief 1-liner summary'}),
            'description': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 4, 'placeholder': 'Detailed materials, craft, dimensions, and specifications'}),
            'price': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': '₹ Selling Price'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control luxury-input', 'placeholder': '₹ Original MRP (optional)'}),
            'stock_count': forms.NumberInput(attrs={'class': 'form-control luxury-input'}),
            'badge': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. LIMITED EDITION'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'https://...'}),
            'material': forms.TextInput(attrs={'class': 'form-control luxury-input'}),
            'care_instructions': forms.TextInput(attrs={'class': 'form-control luxury-input'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'reviewer_city', 'rating', 'title', 'comment']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Your Full Name'}),
            'reviewer_city': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. Mumbai, Bengaluru, Delhi'}),
            'rating': forms.Select(choices=[(5, '★★★★★ (5/5) - Outstanding'), (4, '★★★★☆ (4/5) - Very Good'), (3, '★★★☆☆ (3/5) - Good'), (2, '★★☆☆☆ (2/5) - Average'), (1, '★☆☆☆☆ (1/5) - Disappointing')], attrs={'class': 'form-select luxury-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Review Headline'}),
            'comment': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 3, 'placeholder': 'Share your authentic experience with this piece...'}),
        }


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Aarav Sharma'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'aarav@example.com'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 98765 43210'})
    )
    address_line1 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Flat / House No., Luxury Towers, MG Road'})
    )
    address_line2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Landmark, Area (Optional)'})
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Bengaluru'})
    )
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        widget=forms.Select(attrs={'class': 'form-select luxury-input'})
    )
    pincode = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '560001'})
    )
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control luxury-input text-uppercase', 'placeholder': 'ENTER PROMO CODE'})
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Create strong password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Last Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
