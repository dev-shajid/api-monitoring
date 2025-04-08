"""
Static product data for e-commerce application
"""

products = [
    {
        "id": 1,
        "name": "Samsung Galaxy S23 Ultra",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "brand": "Samsung",
        "price": 1199.99,
        "specification": {
            "display": "6.8-inch Dynamic AMOLED 2X",
            "processor": "Snapdragon 8 Gen 2",
            "ram": "12GB",
            "storage": "256GB",
            "camera": "200MP main + 12MP ultrawide + 10MP telephoto",
            "battery": "5000mAh",
            "operating_system": "Android 13"
        },
        "availability": True,
        "rating": 4.7,
        "color": ["Phantom Black", "Cream", "Green", "Lavender"],
        "usage": "Communication, Photography, Gaming, Work",
        "description": "The Samsung Galaxy S23 Ultra features a 200MP camera system, built-in S Pen, and Snapdragon 8 Gen 2 processor for incredible performance. With its stunning 6.8-inch Dynamic AMOLED 2X display and long-lasting 5000mAh battery, it's designed for those who want the ultimate smartphone experience."
    },
    {
        "id": 2,
        "name": "Apple MacBook Pro 14-inch M3 Pro",
        "category": "Electronics",
        "subcategory": "Laptops",
        "brand": "Apple",
        "price": 1999.99,
        "specification": {
            "display": "14.2-inch Liquid Retina XDR",
            "processor": "Apple M3 Pro",
            "ram": "16GB",
            "storage": "512GB SSD",
            "graphics": "19-core GPU",
            "battery": "Up to 18 hours",
            "operating_system": "macOS Sonoma"
        },
        "availability": True,
        "rating": 4.9,
        "color": ["Space Black", "Silver"],
        "usage": "Professional, Creative Work, Software Development",
        "description": "The 14-inch MacBook Pro with M3 Pro delivers exceptional performance and battery life. With its stunning Liquid Retina XDR display, powerful Apple silicon, and incredible efficiency, it's the perfect tool for creative professionals, developers, and power users who need desktop-class performance in a portable package."
    },
    {
        "id": 3,
        "name": "Sony WH-1000XM5",
        "category": "Electronics",
        "subcategory": "Headphones",
        "brand": "Sony",
        "price": 399.99,
        "specification": {
            "type": "Over-ear",
            "noise_cancellation": "Adaptive Noise Cancellation",
            "battery_life": "Up to 30 hours",
            "connectivity": "Bluetooth 5.2, 3.5mm",
            "microphones": "8 microphones",
            "charging": "USB-C",
            "weight": "250g"
        },
        "availability": True,
        "rating": 4.8,
        "color": ["Black", "Silver"],
        "usage": "Music Listening, Calls, Travel",
        "description": "The Sony WH-1000XM5 headphones offer industry-leading noise cancellation with eight microphones and two processors to control ambient sound. With up to 30 hours of battery life, crystal clear call quality, and premium audio performance, they're perfect for travelers, music enthusiasts, and professionals who need focus."
    },
    {
        "id": 4,
        "name": "Nike Air Zoom Pegasus 40",
        "category": "Footwear",
        "subcategory": "Running Shoes",
        "brand": "Nike",
        "price": 129.99,
        "specification": {
            "type": "Neutral running",
            "cushioning": "Nike Zoom Air",
            "drop": "10mm",
            "weight": "9.0 oz (men's size 10)",
            "upper": "Engineered mesh",
            "outsole": "Rubber",
            "arch_support": "Medium"
        },
        "availability": True,
        "rating": 4.6,
        "color": ["Black/White", "Blue/Orange", "Grey/Volt", "White/Red"],
        "usage": "Running, Training, Casual Wear",
        "description": "The Nike Air Zoom Pegasus 40 continues the legacy of this iconic running shoe with responsive cushioning and breathable support. Featuring Nike Zoom Air units and engineered mesh, it delivers a smooth, stable ride for runners of all levels, from daily training to long distances."
    },
    {
        "id": 5,
        "name": "Instant Pot Duo Plus 6-Quart",
        "category": "Home",
        "subcategory": "Kitchen Appliances",
        "brand": "Instant Pot",
        "price": 129.95,
        "specification": {
            "capacity": "6 Quart",
            "functions": "9-in-1 multi-cooker",
            "modes": ["Pressure Cook", "Slow Cook", "Rice Cooker", "Steamer", "Sauté", "Yogurt Maker", "Sterilizer", "Warmer"],
            "power": "1000W",
            "material": "Stainless Steel",
            "display": "LCD Display",
            "safety_features": "10+ built-in safety features"
        },
        "availability": True,
        "rating": 4.7,
        "color": ["Stainless Steel/Black"],
        "usage": "Cooking, Food Preparation",
        "description": "The Instant Pot Duo Plus is a versatile 9-in-1 multi-cooker that replaces several kitchen appliances. It functions as a pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and more. With 15 one-touch Smart Programs and advanced safety features, it makes cooking quick, easy, and convenient for busy households."
    },
    {
        "id": 6,
        "name": "Dyson V12 Detect Slim",
        "category": "Home",
        "subcategory": "Vacuum Cleaners",
        "brand": "Dyson",
        "price": 649.99,
        "specification": {
            "suction_power": "150 AW",
            "runtime": "Up to 60 minutes",
            "weight": "5.2 lbs",
            "bin_volume": "0.35L",
            "filtration": "HEPA",
            "features": ["Laser Dust Detection", "Piezo Sensor", "LCD Screen", "5-Stage Filtration"]
        },
        "availability": True,
        "rating": 4.8,
        "color": ["Purple/Nickel"],
        "usage": "Home Cleaning, Floor Care",
        "description": "The Dyson V12 Detect Slim vacuum features a laser that reveals microscopic dust, a piezo sensor that sizes and counts dust particles, and an LCD screen that shows what's being sucked up. With powerful suction and a lightweight design, it intelligently adapts to different floor types and provides up to 60 minutes of runtime for whole-home cleaning."
    },
    {
        "id": 7,
        "name": "LG C3 65-inch OLED TV",
        "category": "Electronics",
        "subcategory": "TVs",
        "brand": "LG",
        "price": 1999.99,
        "specification": {
            "display": "65-inch OLED evo",
            "resolution": "4K UHD (3840 x 2160)",
            "processor": "α9 Gen6 AI Processor 4K",
            "refresh_rate": "120Hz",
            "hdr": ["Dolby Vision", "HDR10", "HLG"],
            "gaming_features": ["NVIDIA G-SYNC", "AMD FreeSync", "VRR"],
            "sound": "Virtual 7.1.2 channel sound"
        },
        "availability": True,
        "rating": 4.9,
        "color": ["Black"],
        "usage": "Entertainment, Gaming, Streaming",
        "description": "The LG C3 OLED TV delivers stunning picture quality with perfect blacks and vibrant colors. Powered by the α9 Gen6 AI Processor, it offers exceptional 4K gaming with NVIDIA G-SYNC, AMD FreeSync, and a 120Hz refresh rate. With webOS 23, Dolby Vision and Atmos support, and built-in voice assistants, it provides an immersive entertainment experience for movies, shows, and games."
    },
    {
        "id": 8,
        "name": "Levi's 501 Original Fit Jeans",
        "category": "Clothing",
        "subcategory": "Pants",
        "brand": "Levi's",
        "price": 69.50,
        "specification": {
            "fit": "Original Fit - Straight Leg",
            "rise": "Mid Rise",
            "material": "100% Cotton",
            "closure": "Button Fly",
            "pockets": "5-pocket styling",
            "care": "Machine wash",
            "inseam": "30, 32, 34 inches"
        },
        "availability": True,
        "rating": 4.7,
        "color": ["Dark Stonewash", "Medium Stonewash", "Black", "Light Stonewash"],
        "usage": "Casual Wear, Everyday",
        "description": "The iconic Levi's 501 Original Fit Jeans have been a staple in wardrobes for generations. Made with 100% cotton denim, these straight-leg jeans feature the timeless button fly and 5-pocket styling. Their versatile design makes them easy to dress up or down, perfect for daily wear and built to last through years of use."
    },
    {
        "id": 9,
        "name": "Bose QuietComfort Ultra Earbuds",
        "category": "Electronics",
        "subcategory": "Earbuds",
        "brand": "Bose",
        "price": 299.99,
        "specification": {
            "type": "True Wireless",
            "noise_cancellation": "CustomTune Technology",
            "battery_life": "Up to 6 hours (24 hours with case)",
            "connectivity": "Bluetooth 5.3",
            "water_resistance": "IPX4",
            "charging": "USB-C, Wireless Qi",
            "microphones": "Multiple microphones with noise rejection"
        },
        "availability": True,
        "rating": 4.8,
        "color": ["Black", "White Smoke", "Moonstone Blue"],
        "usage": "Music, Calls, Exercise",
        "description": "Bose QuietComfort Ultra Earbuds deliver world-class noise cancellation and immersive sound in a compact, comfortable design. With up to 6 hours of battery life (24 with the charging case), intuitive touch controls, and impressive call quality, they're perfect for commuters, travelers, and music lovers seeking premium audio without wires."
    },
    {
        "id": 10,
        "name": "The North Face Resolve 2 Jacket",
        "category": "Clothing",
        "subcategory": "Outerwear",
        "brand": "The North Face",
        "price": 89.95,
        "specification": {
            "material": "100% Nylon ripstop",
            "waterproofing": "DWR (Durable Water Repellent) finish",
            "lining": "Mesh lining",
            "hood": "Adjustable, stowable hood",
            "pockets": "Two zippered hand pockets",
            "closure": "Full-zip front with Velcro storm flap",
            "cuffs": "Elastic bound cuffs"
        },
        "availability": True,
        "rating": 4.6,
        "color": ["Black", "Navy", "Red", "Green"],
        "usage": "Outdoor Activities, Hiking, Casual Wear",
        "description": "The North Face Resolve 2 Jacket is a versatile waterproof shell perfect for unpredictable weather. With its adjustable, stowable hood, mesh lining for breathability, and DWR finish to repel moisture, it keeps you protected from wind and rain. Lightweight and packable, it's ideal for hiking, traveling, or everyday use when the weather turns."
    }
]