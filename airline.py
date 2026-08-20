from datetime import datetime, timedelta

# --- Configuration & Mock Database ---
# Flight Inventory
flights = {
    "FL101": {
        "route": "New York to London",
        "total_seats": 100,
        "available_seats": 12,  # Low seats will trigger higher dynamic pricing
        "base_fares": {"Economy": 300.0, "Business": 800.0, "First Class": 1500.0},
        "departure_date": datetime(2026, 9, 15)
    },
    "FL202": {
        "route": "Tokyo to Los Angeles",
        "total_seats": 150,
        "available_seats": 90,  # High seats keep base pricing lower
        "base_fares": {"Economy": 400.0, "Business": 1000.0, "First Class": 2000.0},
        "departure_date": datetime(2026, 10, 30)
    }
}

# Baggage Allowance Rules (Included weight limits per class)
BAGGAGE_RULES = {
    "Economy": {"free_bags": 1, "extra_bag_fee": 50.0},
    "Business": {"free_bags": 2, "extra_bag_fee": 40.0},
    "First Class": {"free_bags": 3, "extra_bag_fee": 0.0}
}


# --- Core System Functions ---

# 1. Flight Search & Seat Availability
def search_flights():
    print("--- Flight Search Results ---")
    for fid, info in flights.items():
        print(f"Flight: {fid} | {info['route']} | Date: {info['departure_date'].strftime('%Y-%m-%d')}")
        print(f"  -> Seats Available: {info['available_seats']}/{info['total_seats']}")
        print(f"  -> Base Prices: Economy: ${info['base_fares']['Economy']} | Business: ${info['base_fares']['Business']} | First Class: ${info['base_fares']['First Class']}\n")


# 2. Dynamic Pricing Engine
def calculate_dynamic_fare(flight_id, seat_class, booking_date, passenger_type):
    flight = flights.get(flight_id)
    if not flight:
        return 0.0
    
    # Factor A: Base Class Fare
    fare = flight["base_fares"].get(seat_class, 300.0)
    
    # Factor B: Seat Availability Surcharge (If less than 15% seats left, price rises 20%)
    capacity_ratio = flight["available_seats"] / flight["total_seats"]
    if capacity_ratio < 0.15:
        fare *= 1.20
        
    # Factor C: Advance Booking Window (Days left until departure)
    days_to_departure = (flight["departure_date"] - booking_date).days
    if days_to_departure < 7:
        fare *= 1.30  # Last-minute booking surcharge (30% extra)
    elif days_to_departure < 30:
        fare *= 1.10  # Medium window surcharge (10% extra)

    # Factor D: Passenger Type Adjustments
    if passenger_type == "Infant":
        fare *= 0.10  # 90% discount for infants
    elif passenger_type == "Senior":
        fare *= 0.90  # 10% discount for senior citizens
        
    return fare


# 3. Baggage Fee Calculation
def calculate_baggage_charges(seat_class, bag_count):
    rules = BAGGAGE_RULES[seat_class]
    if bag_count <= rules["free_bags"]:
        return 0.0
    extra_bags = bag_count - rules["free_bags"]
    return extra_bags * rules["extra_bag_fee"]


# 4. Passenger Booking System
def book_passenger(passenger_name, flight_id, seat_class, passenger_type, bag_count, booking_date):
    print(f"--- Processing Booking for {passenger_name} ---")
    flight = flights.get(flight_id)
    
    # Check seat availability
    if not flight or flight["available_seats"] <= 0:
        print(f"Booking Failed: No seats available on flight {flight_id}.\n")
        return None

    # Compute charges
    ticket_fare = calculate_dynamic_fare(flight_id, seat_class, booking_date, passenger_type)
    baggage_fee = calculate_baggage_charges(seat_class, bag_count)
    total_cost = ticket_fare + baggage_fee
    
    # Deduct seat from inventory
    flight["available_seats"] -= 1
    
    # Create booking record summary
    booking = {
        "name": passenger_name,
        "flight_id": flight_id,
        "class": seat_class,
        "passenger_type": passenger_type,
        "fare": ticket_fare,
        "baggage_fee": baggage_fee,
        "total": total_cost,
        "booking_date": booking_date
    }
    
    print(f"Success! Booking Confirmed.")
    print(f"Ticket Fare (Dynamic): ${ticket_fare:.2f} | Baggage Charges: ${baggage_fee:.2f}")
    print(f"Total Amount Paid: ${total_cost:.2f}\n")
    return booking


# 5. Cancellation & Refund Management
def cancel_booking(booking_record, cancellation_date):
    print(f"--- Processing Cancellation for {booking_record['name']} ---")
    flight_id = booking_record["flight_id"]
    flight = flights[flight_id]
    
    # Return seat back to availability inventory
    flight["available_seats"] += 1
    
    # Refund percentage logic based on how early they cancel
    days_to_departure = (flight["departure_date"] - cancellation_date).days
    
    if days_to_departure >= 14:
        refund_percent = 0.90  # 90% refund if cancelled 2 weeks before flight
    elif days_to_departure >= 3:
        refund_percent = 0.50  # 50% refund if cancelled between 3 to 13 days
    else:
        refund_percent = 0.00  # No refund for last-minute cancellations (under 3 days)
        
    refund_amount = booking_record["fare"] * refund_percent
    print(f"Cancelled {days_to_departure} days before departure.")
    print(f"Refund Calculation Rate: {refund_percent * 100:.0f}% of ticket price.")
    print(f"Amount Refunded to Passenger: ${refund_amount:.2f}\n")


# --- Automated Script Simulation Execution ---

# Step 1: Initial Flight Search
search_flights()

# Step 2: Book a regular Business Class ticket far in advance
booking1 = book_passenger(
    passenger_name="Alice Smith",
    flight_id="FL202",
    seat_class="Business",
    passenger_type="Regular",
    bag_count=4,  # 2 free, 2 extra bags charged
    booking_date=datetime(2026, 8, 1)  # Far in advance
)

# Step 3: Book a last-minute Senior ticket on a flight with low seat counts
booking2 = book_passenger(
    passenger_name="Bob Jones",
    flight_id="FL101",
    seat_class="Economy",
    passenger_type="Senior",
    bag_count=1,  # Fits free allowance
    booking_date=datetime(2026, 9, 12)  # Only 3 days before flight
)

# Step 4: Show current inventory status after bookings are placed
search_flights()

# Step 5: Cancel a ticket and calculate refund
if booking1:
    cancel_booking(booking1, cancellation_date=datetime(2026, 8, 15))

# Step 6: Final check to verify seat returned to pool
search_flights()
