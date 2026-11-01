from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from store.models import Category, Product, ProductImage, ProductVariant, Coupon, Review

class Command(BaseCommand):
    help = 'Seeds database with high-end luxury e-commerce catalog items in Indian Rupees'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Clearing old catalog data..."))
        Review.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Coupon.objects.all().delete()

        # Create demo admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@aurastudio.in', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))

        # Create Coupons
        Coupon.objects.create(
            code="AURA10",
            discount_percentage=Decimal('10.00'),
            min_purchase=Decimal('999.00'),
            description="10% off on all orders above ₹999"
        )
        Coupon.objects.create(
            code="WELCOME500",
            flat_discount=Decimal('500.00'),
            min_purchase=Decimal('2499.00'),
            description="Flat ₹500 off on your order above ₹2,499"
        )
        Coupon.objects.create(
            code="FESTIVE20",
            discount_percentage=Decimal('20.00'),
            min_purchase=Decimal('4999.00'),
            description="Festive Luxe: 20% off on premium purchases above ₹4,999"
        )

        # Categories
        cat_data = [
            {
                "name": "Atelier Apparel",
                "tagline": "Architectural tailoring, handloom silks, and elevated contemporary silhouettes",
                "icon": "bi-person-badge",
                "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=800&auto=format&fit=crop",
                "display_order": 1
            },
            {
                "name": "Haute Horlogerie",
                "tagline": "Precision mechanical chronometers, sapphire crystal & surgical grade stainless steel",
                "icon": "bi-watch",
                "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=800&auto=format&fit=crop",
                "display_order": 2
            },
            {
                "name": "Acoustics & Cyber Tech",
                "tagline": "High-fidelity spatial audio, machined aluminum, and bespoke tactile workspaces",
                "icon": "bi-headphones",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop",
                "display_order": 3
            },
            {
                "name": "Artisanal Fragrance",
                "tagline": "Rare botanical extractions, Kashmiri saffron, royal ambergris and organic agarwood",
                "icon": "bi-droplet-half",
                "image_url": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?q=80&w=800&auto=format&fit=crop",
                "display_order": 4
            },
            {
                "name": "Living & Sculptural Objects",
                "tagline": "Travertine lighting, hand-blown smoky crystal, and tactile organic home goods",
                "icon": "bi-lamp",
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?q=80&w=800&auto=format&fit=crop",
                "display_order": 5
            },
            {
                "name": "Leather & Travel Goods",
                "tagline": "Full-grain Tuscan vegetable-tanned leather handcrafted for modern globetrotters",
                "icon": "bi-bag",
                "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=800&auto=format&fit=crop",
                "display_order": 6
            }
        ]

        cats = {}
        for c in cat_data:
            cat_obj = Category.objects.create(
                name=c["name"],
                tagline=c["tagline"],
                icon=c["icon"],
                image_url=c["image_url"],
                display_order=c["display_order"]
            )
            cats[c["name"]] = cat_obj

        # Products
        products_data = [
            # Apparel
            {
                "category": cats["Atelier Apparel"],
                "name": "Onyx Structured Raw Silk Kimono Trench",
                "brand": "AURA ATELIER",
                "short_description": "Hand-spun Bhagalpur raw silk with a relaxed fluid drape and matte gunmetal toggle closures.",
                "description": "Constructed from artisanal pure raw mulberry silk sourced from ethical weaving collectives in Bihar and tailored in our Bengaluru studio. Features a dropped shoulder cut, deep concealed slip pockets, and a removable self-tie sash with hand-finished bar-tack reinforcements.",
                "price": Decimal('8499.00'),
                "original_price": Decimal('11999.00'),
                "stock_count": 18,
                "badge": "SIGNATURE PIECE",
                "rating": Decimal('4.9'),
                "rating_count": 24,
                "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": True,
                "material": "100% Handloom Raw Silk (280 GSM)",
                "variants": [("Size", "Small (38)"), ("Size", "Medium (40)"), ("Size", "Large (42)"), ("Size", "XL (44)")],
                "reviews": [
                    ("Kabir Mehra", "South Mumbai", 5, "Unmatched drape and weight", "The raw texture of the silk is majestic. Looks sublime over both casual t-shirts and formal kurtas."),
                    ("Ananya Sen", "Kolkata", 5, "Pure luxury craftsmanship", "Every seam is immaculately finished. Arrived in a scented canvas garment bag within 2 days.")
                ]
            },
            {
                "category": cats["Atelier Apparel"],
                "name": "Chalk White Heavyweight Linen Overshirt",
                "brand": "STUDIO KAVACH",
                "short_description": "European flax linen, boxy silhouette with mother-of-pearl buttons and contrast topstitching.",
                "description": "A warm-weather wardrobe essential crafted from 240 GSM organic flax linen. Pre-washed for a buttery soft hand-feel that only gets better with age. Features twin chest flap utility pockets and vented side slits for effortless movement.",
                "price": Decimal('3899.00'),
                "original_price": Decimal('4999.00'),
                "stock_count": 32,
                "badge": "BESTSELLER",
                "rating": Decimal('4.8'),
                "rating_count": 42,
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": False,
                "material": "100% Normandy Flax Linen",
                "variants": [("Size", "S"), ("Size", "M"), ("Size", "L"), ("Size", "XL")],
                "reviews": [
                    ("Rohan Varma", "Bengaluru", 5, "Breathable perfection", "Wore this in 35-degree heat and felt super cool. The texture feels incredibly high-end.")
                ]
            },
            {
                "category": cats["Atelier Apparel"],
                "name": "Pleated Midnight Tapered Trousers",
                "brand": "AURA ATELIER",
                "short_description": "High-rise relaxed taper crafted from tropical wool-tencel blend with double reverse pleats.",
                "description": "Engineered for maximum drape and fluid motion. Features an interior curtain waistband, side tab adjusters that eliminate the need for belts, and an uncuffed clean break hem.",
                "price": Decimal('4499.00'),
                "original_price": Decimal('5999.00'),
                "stock_count": 20,
                "badge": "LIMITED DROP",
                "rating": Decimal('4.7'),
                "rating_count": 19,
                "image_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": True,
                "material": "60% Tropical Wool, 40% Tencel Lyocell",
                "variants": [("Waist", "30 inch"), ("Waist", "32 inch"), ("Waist", "34 inch"), ("Waist", "36 inch")],
                "reviews": [
                    ("Zain Merchant", "Hyderabad", 5, "Tailored elegance", "The drape is unbelievable. Pairs wonderfully with loafers or chunky sneakers.")
                ]
            },

            # Watches
            {
                "category": cats["Haute Horlogerie"],
                "name": "Chronos Obsidian Automatic 40mm",
                "brand": "HORO STUDIOS",
                "short_description": "Miyota 9015 Hi-Beat mechanical movement, sapphire glass, exhibition caseback, and matte ceramic bezel.",
                "description": "An exercise in restrained brutalist horology. Water resistant to 100 meters with screw-down crown, diamond-cut faceted hands, and a custom stealth rotor visible through sapphire crystal. Comes mounted on a supple quick-release FKM fluoroelastomer rubber strap.",
                "price": Decimal('18990.00'),
                "original_price": Decimal('24999.00'),
                "stock_count": 12,
                "badge": "COLLECTOR’S EDITION",
                "rating": Decimal('5.0'),
                "rating_count": 31,
                "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": True,
                "material": "316L Surgical Stainless Steel & Sapphire Crystal",
                "variants": [("Dial Color", "Obsidian Black"), ("Dial Color", "Sunburst Titanium"), ("Dial Color", "Champagne Gold")],
                "reviews": [
                    ("Devansh Kapoor", "New Delhi", 5, "Sublime engineering", "I own Swiss pieces that cost five times more, but the finishing on this dial and the sweep of the 28,800 BPH movement is incredible."),
                    ("Vikram Singhania", "Gurugram", 5, "A real conversation starter", "Everyone at my office asks about this watch. The matte stealth black finish is stunning.")
                ]
            },
            {
                "category": cats["Haute Horlogerie"],
                "name": "Verve Minimalist Rose Gold Mesh Dress Watch",
                "brand": "HORO STUDIOS",
                "short_description": "Ultra-slim 6.8mm profile, Swiss quartz movement with brushed satin champagne dial.",
                "description": "Designed for understated black-tie events and modern formalwear. Accompanied by a hand-woven Milanese stainless steel mesh bracelet with magnetic micro-adjustment lock.",
                "price": Decimal('7499.00'),
                "original_price": Decimal('9999.00'),
                "stock_count": 25,
                "badge": "ELEGANCE EDIT",
                "rating": Decimal('4.8'),
                "rating_count": 16,
                "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": True,
                "material": "PVD Rose Gold, Sapphire Coated Mineral",
                "variants": [("Strap", "Rose Gold Mesh"), ("Strap", "Italian Black Leather")],
                "reviews": [
                    ("Priya Natarajan", "Chennai", 5, "So slim and elegant", "Sits completely flat on the wrist. Looks exceptionally graceful.")
                ]
            },

            # Tech & Acoustics
            {
                "category": cats["Acoustics & Cyber Tech"],
                "name": "Aura Spatial Wireless ANC Over-Ear Headphones",
                "brand": "SONIQUE LABS",
                "short_description": "Custom 45mm beryllium drivers, active spatial tracking, CNC machined anodized earcups, 40h battery.",
                "description": "Audiophile grade frequency response (10Hz - 42kHz) tuned with planar precision. Features 6-microphone hybrid active noise cancellation, lossless LDAC codec transmission, and plush magnetic memory foam lambskin pads for all-day listening fatigue elimination.",
                "price": Decimal('14499.00'),
                "original_price": Decimal('19999.00'),
                "stock_count": 22,
                "badge": "FLAGSHIP TECH",
                "rating": Decimal('4.9'),
                "rating_count": 58,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": True,
                "material": "Aviation Aluminum, Memory Foam, Lambskin Leather",
                "variants": [("Color", "Space Graphite"), ("Color", "Frosted Silver"), ("Color", "Deep Midnight")],
                "reviews": [
                    ("Arjun Nair", "Kochi", 5, "Mind-blowing soundstage", "The separation in instruments on FLAC tracks is pristine. The ANC easily silenced my Mumbai-Delhi flight noise."),
                    ("Siddharth Rao", "Bengaluru", 5, "Better than mainstream brands", "The aluminum tactile dials feel so satisfying compared to fiddly touch controls.")
                ]
            },
            {
                "category": cats["Acoustics & Cyber Tech"],
                "name": "Monolith Oak & Brass Hi-Fi Bluetooth Speaker",
                "brand": "SONIQUE LABS",
                "short_description": "Solid walnut acoustic enclosure, twin silk-dome tweeters and down-firing subwoofer.",
                "description": "Hand-carved from FSC-certified dark walnut timber. Equipped with analog knurled brass bass/treble potentiometers, Bluetooth 5.3 with aptX HD, and analog auxiliary input.",
                "price": Decimal('9999.00'),
                "original_price": Decimal('12999.00'),
                "stock_count": 14,
                "badge": "ACOUSTIC ART",
                "rating": Decimal('4.9'),
                "rating_count": 27,
                "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": False,
                "material": "Solid Walnut & Solid Machined Brass",
                "variants": [("Wood Finish", "Dark American Walnut"), ("Wood Finish", "Natural Scandinavian Oak")],
                "reviews": [
                    ("Kavita Iyer", "Pune", 5, "A sculpture that sings", "Deep, warm bass that fills our living room. It's as much a decorative centerpiece as it is a sound system.")
                ]
            },
            {
                "category": cats["Acoustics & Cyber Tech"],
                "name": "Cipher TKL CNC Mechanical Keyboard",
                "brand": "CYBER CRAFT",
                "short_description": "Gasket-mounted polycarbonate plate, lubed linear switches, hot-swappable PCB, PBT dye-sub caps.",
                "description": "Every key strike delivers an intoxicating, deep acoustic 'thock'. Weighs 1.8kg with an internal brass weight and multi-layer poron dampening foam. Fully programmable via QMK/VIA.",
                "price": Decimal('11299.00'),
                "original_price": Decimal('14500.00'),
                "stock_count": 19,
                "badge": "DESK ESSENTIAL",
                "rating": Decimal('4.9'),
                "rating_count": 33,
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": True,
                "material": "6063 Aluminum, FR4 Plate, Double-Shot PBT",
                "variants": [("Switch Type", "Silent Linear Lubricated"), ("Switch Type", "Tactile Thock 62g")],
                "reviews": [
                    ("Neil Bhattacharya", "Bengaluru", 5, "Coding nirvana", "Typing on this 8 hours a day is pure therapy. The heavy aluminum base doesn't budge an inch.")
                ]
            },

            # Fragrance
            {
                "category": cats["Artisanal Fragrance"],
                "name": "Oud Royale Extrait de Parfum 100ml",
                "brand": "ATELIER PARFUM",
                "short_description": "Wild Assamese oud, smoky birch tar, Turkish damask rose, and bourbon vanilla.",
                "description": "Macerated for 9 months in Grasse and bottled at an intense 32% concentration. Opens with bright spicy cardamom and saffron before melting into dark regal agarwood, aged leather, and a lingering amber warmth that lasts 18+ hours.",
                "price": Decimal('6499.00'),
                "original_price": Decimal('8500.00'),
                "stock_count": 40,
                "badge": "EXTRAIT INTENSE",
                "rating": Decimal('4.9'),
                "rating_count": 76,
                "image_url": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": True,
                "material": "Rare Botanical Essential Oils (32% Extrait Concentration)",
                "variants": [("Size", "50ml Travel Flacon"), ("Size", "100ml Heavy Glass Bottle")],
                "reviews": [
                    ("Sameer Alvi", "Lucknow", 5, "Masterpiece silage", "The Assam oud is authentic, not synthetic. People stop me at weddings to ask what fragrance I'm wearing."),
                    ("Meera Deshmukh", "Mumbai", 5, "Hypnotic and luxurious", "Deep, warm, and sophisticated. The magnetic cap and weighted bottle feel so opulent.")
                ]
            },
            {
                "category": cats["Artisanal Fragrance"],
                "name": "Himalayan Cedar & Vetiver Botanical Elixir",
                "brand": "ATELIER PARFUM",
                "short_description": "Cold-pressed Jojoba, wild Deodar cedarwood, and monsoon khus root oil.",
                "description": "Captures the petrichor of raindrops hitting pine needle forest floors in Himachal. Multipurpose nourishing oil for beard, hair ends, and pulse points.",
                "price": Decimal('1999.00'),
                "original_price": Decimal('2499.00'),
                "stock_count": 55,
                "badge": "ORGANIC HARVEST",
                "rating": Decimal('4.8'),
                "rating_count": 49,
                "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": False,
                "material": "Organic Cold-Pressed Botanical Oils",
                "variants": [("Volume", "60ml Pipette Flacon")],
                "reviews": [
                    ("Gaurav Sethi", "Chandigarh", 5, "Instant nostalgia", "Smells like a morning walk through Shimla pine woods. Absorbs quickly without greasy sheen.")
                ]
            },

            # Living
            {
                "category": cats["Living & Sculptural Objects"],
                "name": "Sculpted Italian Travertine Table Lamp",
                "brand": "CASA AURA",
                "short_description": "Natural unfilled Roman travertine stone pillar with matte linen drum diffuser.",
                "description": "Each stone base features organic voids and vein textures unique to its geological quarry block. Casts a comforting 2700K golden glow perfect for bedside credenzas and minimalist living rooms.",
                "price": Decimal('6899.00'),
                "original_price": Decimal('8999.00'),
                "stock_count": 15,
                "badge": "HAND-HEWN STONE",
                "rating": Decimal('4.9'),
                "rating_count": 18,
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": False,
                "material": "Natural Roman Travertine Stone & Textured Raw Linen",
                "variants": [("Stone Shade", "Warm Ivory Travertine"), ("Stone Shade", "Dark Silver Travertine")],
                "reviews": [
                    ("Tara Singhal", "Jaipur", 5, "Art gallery quality", "Substantial weight, incredible stone tactile texture. Transforms our entire lounge ambient lighting.")
                ]
            },
            {
                "category": cats["Living & Sculptural Objects"],
                "name": "Smoked Mouth-Blown Crystal Decanter Set",
                "brand": "CASA AURA",
                "short_description": "Includes 1.2L aerating decanter and 4 faceted lowball tumblers with amber obsidian tint.",
                "description": "Master artisan flame-worked borosilicate crystal with lead-free clarity. Weighted base designed to swirl your favorite single malts or filtered infusions without spill risk.",
                "price": Decimal('4999.00'),
                "original_price": Decimal('6499.00'),
                "stock_count": 28,
                "badge": "ENTERTAINING",
                "rating": Decimal('4.7'),
                "rating_count": 22,
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": True,
                "material": "Hand-Blown Smoked Borosilicate Crystal",
                "variants": [("Set Type", "Decanter + 4 Tumblers"), ("Set Type", "Decanter Only (1.2L)")],
                "reviews": [
                    ("Rahul Khurana", "Delhi NCR", 5, "Stunning barware", "The smoked amber shade looks incredible under evening warm lighting.")
                ]
            },

            # Leather & Travel
            {
                "category": cats["Leather & Travel Goods"],
                "name": "The Equinox Vegetable Tanned 48H Weekender",
                "brand": "KRAFT & SULLIVAN",
                "short_description": "Full-grain pull-up cowhide, solid brass YKK Excella zippers, separate ventilated footwear vault.",
                "description": "Handcrafted to comply with all domestic airline overhead cabin dimensions (IndiGo, Air India, Vistara). Internal neoprene padded 16-inch laptop partition, water-resistant twill lining, and an ergonomic leather shoulder strap.",
                "price": Decimal('12499.00'),
                "original_price": Decimal('16999.00'),
                "stock_count": 16,
                "badge": "HERITAGE LEATHER",
                "rating": Decimal('5.0'),
                "rating_count": 48,
                "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=800&auto=format&fit=crop",
                "is_featured": True,
                "is_trending": True,
                "material": "Certified Full-Grain Pull-Up Leather (Develops Patina)",
                "variants": [("Colorway", "Bourbon Cognac"), ("Colorway", "Matte Noir"), ("Colorway", "Espresso Brown")],
                "reviews": [
                    ("Aditya Bansal", "Ahmedabad", 5, "Built to last a lifetime", "Took this on three international trips already. Leather smells rich and is already picking up a handsome patina."),
                    ("Tanvi Goswami", "Bengaluru", 5, "Worth every single rupee", "The separate shoe compartment is genius. Truly airport luxury.")
                ]
            },
            {
                "category": cats["Leather & Travel Goods"],
                "name": "The Minimalist Bi-Fold RFID Card Vault",
                "brand": "KRAFT & SULLIVAN",
                "short_description": "Laser-cut Horween leather, holds 8 cards + folded Indian currency notes with zero pocket bulk.",
                "description": "Measuring only 5mm when empty. Lined with aerospace Faraday mesh to guard contactless cards from unauthorized skimming. Finished with burnished and hand-waxed edge painting.",
                "price": Decimal('1799.00'),
                "original_price": Decimal('2499.00'),
                "stock_count": 60,
                "badge": "DAILY ESSENTIAL",
                "rating": Decimal('4.8'),
                "rating_count": 63,
                "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?q=80&w=800&auto=format&fit=crop",
                "is_featured": False,
                "is_trending": False,
                "material": "Top Grain Horween Leather & RFID Shielding",
                "variants": [("Color", "Saddle Tan"), ("Color", "Stealth Charcoal"), ("Color", "Hunter Olive")],
                "reviews": [
                    ("Manish Joshi", "Surat", 5, "Slimmest wallet I have ever owned", "Fits ₹500 currency notes cleanly and barely makes a silhouette in slim trousers.")
                ]
            }
        ]

        for p_data in products_data:
            variants = p_data.pop("variants", [])
            reviews = p_data.pop("reviews", [])
            prod = Product.objects.create(**p_data)

            # Add variants
            for v_name, v_val in variants:
                ProductVariant.objects.create(
                    product=prod,
                    name=v_name,
                    value=v_val,
                    stock=12
                )

            # Add reviews
            for r_name, r_city, r_stars, r_title, r_text in reviews:
                Review.objects.create(
                    product=prod,
                    reviewer_name=r_name,
                    reviewer_city=r_city,
                    rating=r_stars,
                    title=r_title,
                    comment=r_text,
                    verified_purchase=True
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(products_data)} luxury products, categories, coupons, and verified reviews!"))
