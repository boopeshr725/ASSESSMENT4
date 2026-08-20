# --- Configuration Constants ---
inventory_stock = {
    "PROD01": True,   # Electronics (In stock)
    "PROD02": False,  # Accessories (Out of stock)
    "PROD03": True,   # Stationery (In stock)
    "PROD04": True    # Luxury Item (In stock)
}

valid_coupons = {"WELCOME5": 5.0, "SUPER10": 10.0}
MAX_DISCOUNT_LIMIT = 100.0
FREE_SHIPPING_THRESHOLD = 500.0
STANDARD_SHIPPING_CHARGE = 15.0

# --- Core Order Processing Logic ---
def process_order(order_items, applied_coupon):
    subtotal = 0.0
    total_item_discount = 0.0
    total_category_discount = 0.0
    total_bulk_discount = 0.0
    total_gst = 0.0
    
    # Process each item in the order
    for item in order_items:
        pid = item.get("id")
        qty = item.get("quantity", 0)
        price = item.get("unit_price", 0.0)
        discount = item.get("discount", 0.0)
        tax_rate = item.get("tax_rate", 0.0)
        category = item.get("category", "")

        # 1. Handle Invalid Product (Not in inventory)
        if pid not in inventory_stock:
            return f"Error: Invalid product ID {pid}."
            
        # 2. Handle Out-of-stock products
        if not inventory_stock[pid]:
            return f"Error: Product {pid} is out of stock."
            
        # 3. Handle Negative or Zero quantities
        if qty < 0:
            return "Error: Negative quantity is invalid."
        if qty == 0:
            return "Error: Quantity cannot be zero."

        # Calculation steps
        item_subtotal = qty * price
        subtotal += item_subtotal
        total_item_discount += discount
        
        # Category discount (5% for Electronics)
        if category == "Electronics":
            total_category_discount += item_subtotal * 0.05
            
        # Bulk-order discount (10% off for qty > 10)
        if qty > 10:
            total_bulk_discount += item_subtotal * 0.10
            
        # Tax (GST) calculation
        total_gst += item_subtotal * tax_rate

    # Handle Coupon codes
    coupon_discount = 0.0
    if applied_coupon:
        if applied_coupon in valid_coupons:
            coupon_discount = valid_coupons[applied_coupon]
        else:
            return f"Error: Invalid coupon code '{applied_coupon}'."

    # Handle Maximum discount limits
    total_discounts = total_item_discount + total_category_discount + total_bulk_discount + coupon_discount
    if total_discounts > MAX_DISCOUNT_LIMIT:
        total_discounts = MAX_DISCOUNT_LIMIT

    # Handle Free shipping thresholds
    shipping_charge = 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD else STANDARD_SHIPPING_CHARGE

    # Calculate Final Amount
    final_amount = subtotal - total_discounts + total_gst + shipping_charge
    return f"Success! Final Amount: ${final_amount:.2f} (Subtotal: ${subtotal:.2f}, Tax: ${total_gst:.2f}, Shipping: ${shipping_charge:.2f})"


# --- Automated QA Test Suite (20 Combinations) ---
test_cases = [
    # 1. Single product
    {"desc": "Single product (Standard)", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": ""},
    
    # 2. Multiple products
    {"desc": "Multiple products", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 50.0, "discount": 0.0, "tax_rate": 0.10}, {"id": "PROD03", "category": "Stationery", "quantity": 2, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.05}], "coupon": ""},
    
    # 3. Zero quantity
    {"desc": "Zero quantity check", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 0, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": ""},
    
    # 4. Negative quantity
    {"desc": "Negative quantity check", "items": [{"id": "PROD01", "category": "Electronics", "quantity": -5, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": ""},
    
    # 5. Invalid product
    {"desc": "Invalid product ID", "items": [{"id": "FALSE_ID", "category": "Electronics", "quantity": 1, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": ""},
    
    # 6. Invalid coupon
    {"desc": "Invalid coupon applied", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": "FAKECODE"},
    
    # 7. Maximum discount limit
    {"desc": "Maximum discount cap test", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 2000.0, "discount": 200.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 8. Tax calculation
    {"desc": "Tax calculation validation", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 2, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.15}], "coupon": ""},
    
    # 9. Free shipping trigger
    {"desc": "Free shipping triggered", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 6, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 10. Bulk order trigger
    {"desc": "Bulk order discount active", "items": [{"id": "PROD03", "category": "Stationery", "quantity": 15, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 11. Out of stock item
    {"desc": "Out of stock check", "items": [{"id": "PROD02", "category": "Accessories", "quantity": 1, "unit_price": 15.0, "discount": 0.0, "tax_rate": 0.05}], "coupon": ""},
    
    # 12. Combo: Single product + valid coupon
    {"desc": "Single product + Valid coupon", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 50.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": "WELCOME5"},
    
    # 13. Combo: Multiple items + valid coupon
    {"desc": "Multiple items + Valid coupon", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 50.0, "discount": 0.0, "tax_rate": 0.0}, {"id": "PROD03", "category": "Stationery", "quantity": 1, "unit_price": 20.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": "SUPER10"},
    
    # 14. Combo: Free shipping + valid coupon
    {"desc": "Free shipping + Valid coupon", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 10, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": "SUPER10"},
    
    # 15. Combo: Bulk order + Category discount
    {"desc": "Bulk order + Category discount", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 12, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 16. Combo: Free shipping + Bulk order
    {"desc": "Free shipping + Bulk order", "items": [{"id": "PROD03", "category": "Stationery", "quantity": 60, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 17. Combo: Tax calculation + Free shipping
    {"desc": "Tax + Free shipping", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 6, "unit_price": 100.0, "discount": 0.0, "tax_rate": 0.10}], "coupon": ""},
    
    # 18. Combo: Bulk order + Negative quantity error check
    {"desc": "Bulk quantity + Negative item error", "items": [{"id": "PROD03", "category": "Stationery", "quantity": 15, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}, {"id": "PROD01", "category": "Electronics", "quantity": -1, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 19. Combo: Multiple items + One invalid product
    {"desc": "Multiple items + One invalid ID", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}, {"id": "FALSE_ID", "category": "Stationery", "quantity": 1, "unit_price": 10.0, "discount": 0.0, "tax_rate": 0.0}], "coupon": ""},
    
    # 20. Combo: Max discount cap + Free shipping + Coupon
    {"desc": "Max discount + Free shipping + Coupon", "items": [{"id": "PROD01", "category": "Electronics", "quantity": 20, "unit_price": 100.0, "discount": 50.0, "tax_rate": 0.05}], "coupon": "SUPER10"}
]

# --- Execute Tests ---
print("==================================================")
print("             RUNNING AUTOMATED QA TESTS           ")
print("==================================================")

for index, case in enumerate(test_cases, start=1):
    result = process_order(case["items"], case["coupon"])
    print(f"Test #{index:02d} [{case['desc']}]:\n -> {result}\n")
    
print("==================================================")
print("             ALL 20 TEST CASES EXECUTED           ")
print("==================================================")
