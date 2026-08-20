# --- Hardcoded Data Configuration ---

# 1. Product Inventory Status (to handle out-of-stock)
inventory_stock = {
    "PROD01": True,   # Laptop (In stock)
    "PROD02": False,  # Phone case (Out of stock)
    "PROD03": True    # Notebooks (In stock - Bulk order)
}

# 2. Multiple products in the current order
order_items = [
    {"id": "PROD01", "category": "Electronics", "quantity": 1, "unit_price": 800.0, "discount": 50.0, "tax_rate": 0.18},
    {"id": "PROD02", "category": "Accessories", "quantity": 2, "unit_price": 15.0, "discount": 0.0, "tax_rate": 0.05},
    {"id": "PROD03", "category": "Stationery", "quantity": 12, "unit_price": 5.0, "discount": 0.0, "tax_rate": 0.12}
]

# 3. Coupon details
applied_coupon = "SUPER10"
valid_coupons = {"WELCOME5": 5.0, "SUPER10": 10.0}  # Code: Discount amount

# 4. Business rules thresholds
MAX_DISCOUNT_LIMIT = 100.0
FREE_SHIPPING_THRESHOLD = 500.0
STANDARD_SHIPPING_CHARGE = 15.0


# --- Order Processing Calculations ---

subtotal = 0.0
total_item_discount = 0.0
total_category_discount = 0.0
total_bulk_discount = 0.0
total_gst = 0.0

print("--- Processing Order Items ---")

for item in order_items:
    pid = item["id"]
    
    # Handle Out-of-stock products
    if not inventory_stock.get(pid, False):
        print(f"Skipped {pid}: Product is out of stock.")
        continue
        
    # Calculate initial item total
    item_subtotal = item["quantity"] * item["unit_price"]
    subtotal += item_subtotal
    
    # Basic item discount
    total_item_discount += item["discount"]
    
    # Handle Category-specific discount (e.g., 5% off Electronics)
    if item["category"] == "Electronics":
        cat_discount = item_subtotal * 0.05
        total_category_discount += cat_discount
        
    # Handle Bulk-order discounts (e.g., 10% off for buying more than 10 items)
    if item["quantity"] > 10:
        bulk_discount = item_subtotal * 0.10
        total_bulk_discount += bulk_discount
        
    # Calculate GST (Tax) for this product
    total_gst += item_subtotal * item["tax_rate"]
    
    print(f"Processed {pid} ({item['category']}): Qty {item['quantity']} | Subtotal: ${item_subtotal:.2f}")

print("\n--- Summary Calculations ---")

# Handle Coupon codes
coupon_discount = 0.0
if applied_coupon in valid_coupons:
    coupon_discount = valid_coupons[applied_coupon]
    print(f"Coupon '{applied_coupon}' applied: -${coupon_discount:.2f}")
else:
    print(f"Warning: Coupon '{applied_coupon}' is invalid.")

# Calculate and handle Maximum discount limits
total_discounts = total_item_discount + total_category_discount + total_bulk_discount + coupon_discount
if total_discounts > MAX_DISCOUNT_LIMIT:
    print(f"Notice: Total discount capped at maximum limit of ${MAX_DISCOUNT_LIMIT:.2f}")
    total_discounts = MAX_DISCOUNT_LIMIT

# Handle Free shipping thresholds
if subtotal >= FREE_SHIPPING_THRESHOLD:
    shipping_charge = 0.0
    print(f"Free shipping applied! (Subtotal ${subtotal:.2f} >= ${FREE_SHIPPING_THRESHOLD:.2f})")
else:
    shipping_charge = STANDARD_SHIPPING_CHARGE

# Calculate Final Amount
final_amount = subtotal - total_discounts + total_gst + shipping_charge


# --- Final Output Receipt ---
print("\n==============================")
print("        ORDER RECEIPT        ")
print("==============================")
print(f"Subtotal:             ${subtotal:.2f}")
print(f"Category Discount:   -${total_category_discount:.2f}")
print(f"Bulk Discount:       -${total_bulk_discount:.2f}")
print(f"Coupon Discount:     -${coupon_discount:.2f}")
print(f"Total Applied Saved: -${total_discounts:.2f}")
print(f"GST (Tax):            ${total_gst:.2f}")
print(f"Shipping Charge:      ${shipping_charge:.2f}")
print("------------------------------")
print(f"Final Amount Due:     ${final_amount:.2f}")
print("==============================")
