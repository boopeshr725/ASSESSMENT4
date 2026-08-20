from datetime import datetime, timedelta

# --- Configuration & Rates ---
# A small layout to trigger conditions like "Full parking lot" easily
parking_slots = {
    "Bike": ["B1"],
    "Standard": ["S1"],  # For Car, SUV
    "Large": ["L1"],     # For Truck
    "EV": ["E1"]         # For Electric Vehicle
}

active_parking = {}  # Tracks database current state {slot_id: vehicle_info}

BASE_RATES = {
    "Bike": 10.0,
    "Car": 20.0,
    "SUV": 30.0,
    "Truck": 50.0,
    "Electric Vehicle": 25.0
}

# --- Core Management System Functions ---

def book_entry(plate, vehicle_type, entry_time):
    # Check for Duplicate vehicle registration
    for slot, info in active_parking.items():
        if info["plate"] == plate:
            return "Error: Duplicate vehicle plate detected"

    # Map vehicle type to correct category slot
    if vehicle_type == "Bike":
        slot_type = "Bike"
    elif vehicle_type in ["Car", "SUV"]:
        slot_type = "Standard"
    elif vehicle_type == "Truck":
        slot_type = "Large"
    elif vehicle_type == "Electric Vehicle":
        slot_type = "EV"
    else:
        return "Error: Wrong vehicle-slot combination"

    # Find available slot
    allocated_slot = None
    for slot in parking_slots.get(slot_type, []):
        if slot not in active_parking:
            allocated_slot = slot
            break

    if not allocated_slot:
        return "Error: Full parking lot for this vehicle category"

    # Store entry record
    active_parking[allocated_slot] = {
        "plate": plate,
        "type": vehicle_type,
        "entry_time": entry_time
    }
    return f"Success: Allocated slot {allocated_slot}"


def process_exit(plate, exit_time, ticket_lost=False, ev_charged=False):
    # Find slot by plate string match
    target_slot = None
    for slot, info in active_parking.items():
        if info["plate"] == plate:
            target_slot = slot
            break

    if not target_slot:
        return "Error: No matching vehicle entry record found"

    ticket = active_parking.pop(target_slot)
    
    # Test Scenario: Lost ticket condition checks
    if ticket_lost:
        return f"Success: Exit processed with Lost Ticket fee. Total: $150.00"

    duration = exit_time - ticket["entry_time"]
    hours = duration.total_seconds() / 3600.0

    # Test Scenario: Early exit check (Grace period under 15 minutes)
    if duration <= timedelta(minutes=15):
        return f"Success: Early exit grace period applied. Total: $0.00"

    # Compute hourly totals rounded up to next integer ceiling 
    hours_charge = max(1, int(hours) + (1 if hours % 1 > 0 else 0))
    rate = BASE_RATES.get(ticket["type"], 20.0)
    total_fee = hours_charge * rate

    # Test Scenario: Peak-hour pricing check
    if (8 <= ticket["entry_time"].hour <= 10) or (17 <= exit_time.hour <= 19):
        total_fee *= 1.5

    # Test Scenario: EV charging fee addition
    if ticket["type"] == "Electric Vehicle" and ev_charged:
        total_fee += 15.0  # Flat flat charging standard fee

    return f"Success: Exit slot {target_slot}. Total Charged: ${total_fee:.2f} for {hours_charge} hrs"


# --- QA Automation Test Suite Runner ---
print("=========================================================================")
print("                   PARKING MANAGEMENT SYSTEM - QA REPORT                 ")
print("=========================================================================\n")

# Test 1: Successful Entry
print("[TEST 1] Successful Slot Allocation")
print(book_entry("CAR-111", "Car", datetime(2026, 8, 20, 12, 0)))
print("")

# Test 2: Full Parking Lot 
print("[TEST 2] Full Parking Lot Verification")
print(book_entry("SUV-222", "SUV", datetime(2026, 8, 20, 12, 5))) # Tries to grab standard slot which is full
print("")

# Test 3: Wrong Vehicle-Slot Combination
print("[TEST 3] Wrong Vehicle Type Verification")
print(book_entry("PLANE-9", "Airplane", datetime(2026, 8, 20, 12, 10)))
print("")

# Test 4: Duplicate Vehicle entry check
print("[TEST 4] Duplicate Vehicle Check")
print(book_entry("CAR-111", "Car", datetime(2026, 8, 20, 12, 15)))
print("")

# Test 5: Early Exit
print("[TEST 5] Early Exit Grace Period Check")
print(book_entry("BIKE-12", "Bike", datetime(2026, 8, 20, 13, 0)))
print(process_exit("BIKE-12", datetime(2026, 8, 20, 13, 10))) # Out within 10 minutes
print("")

# Test 6: Lost Ticket
print("[TEST 6] Lost Ticket Flag Penalty Calculation")
print(process_exit("CAR-111", datetime(2026, 8, 20, 15, 0), ticket_lost=True))
print("")

# Test 7: Peak-Hour Pricing Evaluation
print("[TEST 7] Peak-Hour Pricing Check")
print(book_entry("CAR-777", "Car", datetime(2026, 8, 20, 8, 30))) # 8:30 AM is peak hour
print(process_exit("CAR-777", datetime(2026, 8, 20, 10, 30)))    # 2 hours * $20 * 1.5 peak fee
print("")

# Test 8: EV Charging Fee Calculation
print("[TEST 8] EV Charging Utility Surcharge")
print(book_entry("EV-888", "Electric Vehicle", datetime(2026, 8, 20, 12, 0)))
print(process_exit("EV-888", datetime(2026, 8, 20, 14, 0), ev_charged=True)) # 2 hours * $25 + $15 charging
print("")

# Test 9: Overnight Parking Validation
print("[TEST 9] Overnight Parking Check")
print(book_entry("TRUCK-99", "Truck", datetime(2026, 8, 20, 22, 0))) # Enters 10 PM
print(process_exit("TRUCK-99", datetime(2026, 8, 21, 6, 0)))          # Exits 6 AM next day (8 hours)
print("")

print("=========================================================================")
print("                      ALL QA TESTS COMPLETED SAFELY                      ")
print("=========================================================================")
