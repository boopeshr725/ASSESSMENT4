from datetime import datetime, timedelta

# --- Configuration & Rates ---
# Available slots tracking
parking_slots = {
    "Bike": ["B1", "B2"],
    "Standard": ["S1", "S2"],          # For Car, SUV, and Electric Vehicle
    "Large": ["L1"],                   # For Trucks
    "VIP": ["V1"]                      # Reserved for VIP members
}

# Occupancy database {slot_id: vehicle_data_dict}
active_parking = {}

# Base rates per hour based on vehicle type
BASE_HOURLY_RATES = {
    "Bike": 10.0,
    "Car": 20.0,
    "SUV": 30.0,
    "Truck": 50.0,
    "Electric Vehicle": 25.0
}

# --- Core Management System Functions ---

# 1. Automatic Slot Allocation & Vehicle Entry
def vehicle_entry(plate, vehicle_type, is_vip, entry_time):
    print(f"--- Vehicle Entry Request: {plate} ({vehicle_type}) ---")
    
    # Check VIP status first to allocate a premium spot
    if is_vip:
        slot_type = "VIP"
    elif vehicle_type == "Bike":
        slot_type = "Bike"
    elif vehicle_type in ["Car", "SUV", "Electric Vehicle"]:
        slot_type = "Standard"
    elif vehicle_type == "Truck":
        slot_type = "Large"
    else:
        print("Error: Unknown vehicle type.\n")
        return None

    # Find an open slot in the selected category
    available_list = parking_slots[slot_type]
    allocated_slot = None
    
    for slot in available_list:
        if slot not in active_parking:
            allocated_slot = slot
            break
            
    # Fallback: If VIP slot is full, VIP can look in Standard spots
    if not allocated_slot and is_vip:
        for slot in parking_slots["Standard"]:
            if slot not in active_parking:
                allocated_slot = slot
                break

    if not allocated_slot:
        print(f"Entry Denied: No available slots for {vehicle_type} category.\n")
        return None

    # Register active parking ticket entry
    active_parking[allocated_slot] = {
        "plate": plate,
        "type": vehicle_type,
        "is_vip": is_vip,
        "entry_time": entry_time
    }
    
    print(f"Success: Allocated Slot {allocated_slot} for {plate}.")
    print(f"Entry Time logged: {entry_time.strftime('%H:%M')}\n")
    return allocated_slot


# 2. Dynamic Pricing Engine & Vehicle Exit
def vehicle_exit(slot_id, exit_time, ticket_lost=False):
    if slot_id not in active_parking:
        print(f"Error: No vehicle found parked in slot {slot_id}.\n")
        return

    ticket = active_parking.pop(slot_id)
    plate = ticket["plate"]
    v_type = ticket["type"]
    entry_time = ticket["entry_time"]
    
    print(f"--- Vehicle Exit Request: Slot {slot_id} ({plate}) ---")

    # Handle Lost Ticket Penalty directly
    if ticket_lost:
        lost_ticket_penalty = 150.0
        print(f"Ticket Status: LOST. Flat penalty rate applied: ${lost_ticket_penalty:.2f}")
        print(f"Final Total Due: ${lost_ticket_penalty:.2f}\n")
        return

    # Calculate hours parked (minimum 1 hour rounding rule)
    duration_delta = exit_time - entry_time
    hours_parked = max(1, round(duration_delta.total_seconds() / 3600))
    
    # Rule A: Calculate Base Fee
    base_rate = BASE_HOURLY_RATES.get(v_type, 20.0)
    total_fee = hours_parked * base_rate
    print(f"Duration: {hours_parked} Hour(s) | Base Rate: ${base_rate:.2f}/hr")

    # Rule B: Peak-Hour Pricing Surge Multiply (e.g., Morning rush between 8 AM and 10 AM)
    # Check if either entry hour or exit hour falls in peak windows
    if (8 <= entry_time.hour <= 10) or (17 <= exit_time.hour <= 19):
        total_fee *= 1.5
        print("Rule Applied: Peak-Hour Surcharge active (1.5x Multiplier)")

    # Rule C: VIP Parking Benefit Discounter
    if ticket["is_vip"]:
        total_fee *= 0.80  # 20% flat discount for VIP members
        print("Rule Applied: VIP Membership Discount (20% Off base charges)")

    # Rule D: Eco Incentive Discount
    if v_type == "Electric Vehicle":
        total_fee -= 5.0  # $5 green discount
        total_fee = max(0.0, total_fee)
        print("Rule Applied: Eco Friendly Vehicle Incentive (-$5.00)")

    print(f"Final Total Due: ${total_fee:.2f}\n")


# --- Automated Parking Simulation Execution ---

# Setup sample times
base_day = datetime(2026, 8, 20)
morning_peak_entry = datetime(2026, 8, 20, 8, 30)      # Inside 8-10 AM peak window
standard_entry     = datetime(2026, 8, 20, 12, 00)     # Normal off-peak hours

print("=========================================================")
# Case 1: Standard Car entry & exit (Off-peak)
slot_car = vehicle_entry("CAR-999", "Car", is_vip=False, entry_time=standard_entry)
vehicle_exit(slot_car, exit_time=standard_entry + timedelta(hours=3))

# Case 2: Peak Hour entry for an SUV
slot_suv = vehicle_entry("SUV-123", "SUV", is_vip=False, entry_time=morning_peak_entry)
vehicle_exit(slot_suv, exit_time=morning_peak_entry + timedelta(hours=2))

# Case 3: VIP Member booking slot
slot_vip = vehicle_entry("VIP-777", "Car", is_vip=True, entry_time=standard_entry)
vehicle_exit(slot_vip, exit_time=standard_entry + timedelta(hours=4))

# Case 4: Electric Vehicle with Eco Discount
slot_ev = vehicle_entry("EV-GREEN", "Electric Vehicle", is_vip=False, entry_time=standard_entry)
vehicle_exit(slot_ev, exit_time=standard_entry + timedelta(hours=2))

# Case 5: Lost Ticket Handling Situation
slot_lost = vehicle_entry("LOST-55", "Bike", is_vip=False, entry_time=standard_entry)
vehicle_exit(slot_lost, exit_time=standard_entry + timedelta(hours=1), ticket_lost=True)

# Case 6: Slot Allocation Failure Test (Fill up Large slots with trucks)
slot_truck1 = vehicle_entry("TRUCK-01", "Truck", is_vip=False, entry_time=standard_entry)
slot_truck2 = vehicle_entry("TRUCK-02", "Truck", is_vip=False, entry_time=standard_entry) # Should fail
print("=========================================================")
