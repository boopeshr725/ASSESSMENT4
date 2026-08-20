from datetime import datetime

# --- Mock Flight Database State ---
flights = {
    "FL101": {
        "route": "New York to London",
        "total_seats": 2,          # Small number to test fully booked flight easily
        "available_seats": 2,
        "base_fares": {"Economy": 300.0, "Business": 800.0},
        "departure_date": datetime(2026, 9, 15)
    }
}

active_bookings = {}  # Tracks database bookings by Passenger Name

# --- System Functions ---
def calculate_fare(flight_id, seat_class, booking_date, passenger_type):
    flight = flights.get(flight_id)
    fare = flight["base_fares"].get(seat_class, 300.0)
    
    # Dynamic Pricing: 20% surge if only 1 seat remains (less than 50% capacity)
    if flight["available_seats"] <= 1:
        fare *= 1.20
        
    # Dynamic Pricing: 30% surge if booking within 7 days of departure
    days_left = (flight["departure_date"] - booking_date).days
    if days_left < 7:
        fare *= 1.30
        
    # Passenger Type Discount
    if passenger_type == "Senior":
        fare *= 0.90  # 10% discount
        
    return fare

def calculate_baggage(seat_class, bags):
    free_allowance = 2 if seat_class == "Business" else 1
    if bags <= free_allowance:
        return 0.0
    return (bags - free_allowance) * 50.0  # $50 per extra bag

def book_flight(name, flight_id, seat_class, passenger_type, bags, booking_date):
    if not name or passenger_type not in ["Regular", "Senior"]:
        return "Error: Invalid passenger data"
        
    if name in active_bookings:
        return "Error: Double booking detected for this passenger"
        
    flight = flights.get(flight_id)
    if flight["available_seats"] <= 0:
        return "Error: Flight is fully booked"
        
    fare = calculate_fare(flight_id, seat_class, booking_date, passenger_type)
    baggage_fee = calculate_baggage(seat_class, bags)
    
    # Deduct seat from inventory
    flight["available_seats"] -= 1
    
    # Save active booking
    active_bookings[name] = {
        "flight_id": flight_id,
        "fare": fare,
        "baggage_fee": baggage_fee,
        "total": fare + baggage_fee
    }
    return f"Success: Booking confirmed for {name}. Total Charged: ${fare + baggage_fee:.2f}"

def cancel_flight(name, cancellation_date):
    if name not in active_bookings:
        return "Error: No active booking found"
        
    booking = active_bookings.pop(name)
    flight = flights[booking["flight_id"]]
    
    # Return seat to pool
    flight["available_seats"] += 1
    
    # Refund percentage
    days_left = (flight["departure_date"] - cancellation_date).days
    refund_rate = 0.90 if days_left >= 10 else 0.50
    refund = booking["fare"] * refund_rate
    
    return f"Success: Cancelled. Refund Amount: ${refund:.2f} ({refund_rate*100:.0f}% returned)"


# --- QA Automation Test Suite Runner ---
print("=========================================================================")
print("                   AIRLINE RESERVATION SYSTEM - QA REPORT               ")
print("=========================================================================\n")

# Test 1: Successful Booking
print("[TEST 1] Successful Booking")
res1 = book_flight("Alice", "FL101", "Economy", "Regular", 1, datetime(2026, 8, 1))
print(f"Result -> {res1}\n")

# Test 2: Double Booking
print("[TEST 2] Double Booking")
res2 = book_flight("Alice", "FL101", "Economy", "Regular", 1, datetime(2026, 8, 1))
print(f"Result -> {res2}\n")

# Test 3: Excess Baggage Charges
print("[TEST 3] Excess Baggage")
res3 = book_flight("Bob", "FL101", "Economy", "Regular", 3, datetime(2026, 8, 1)) # 2 extra bags
print(f"Result -> {res3}\n")

# Test 4: Fully Booked Flight
print("[TEST 4] Fully Booked Flight")
res4 = book_flight("Charlie", "FL101", "Economy", "Regular", 1, datetime(2026, 8, 1))
print(f"Result -> {res4}\n")

# Test 5: Cancellation
print("[TEST 5] Cancellation")
res5 = cancel_flight("Alice", datetime(2026, 8, 5))
print(f"Result -> {res5}\n")

# Test 6: Refund Validation
print("[TEST 6] Refund Verification (Late Cancellation vs Early)")
# Re-booking Bob last minute to check a different window later if needed
res6 = cancel_flight("Bob", datetime(2026, 9, 12)) # Only 3 days left = 50% refund
print(f"Result -> {res6}\n")

# Test 7: Invalid Passenger
print("[TEST 7] Invalid Passenger")
res7 = book_flight("", "FL101", "Economy", "AlienType", 1, datetime(2026, 8, 1))
print(f"Result -> {res7}\n")

# Test 8: Dynamic Fare Calculation
print("[TEST 8] Dynamic Fare Calculation (Last-Minute + Senior combo)")
res8 = book_flight("David", "FL101", "Business", "Senior", 2, datetime(2026, 9, 12))
print(f"Result -> {res8}\n")

print("=========================================================================")
print("                      ALL QA TESTS COMPLETED SAFELY                      ")
print("=========================================================================")
