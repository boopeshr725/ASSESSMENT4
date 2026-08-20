# --- Configuration & Rates ---
BASE_CONSULTATION_RATE = 50.0  # Per hour rate
LAB_TEST_PRICES = {"Blood Test": 20.0, "X-Ray": 50.0, "MRI": 200.0}
MEDICINE_PRICES = {"Aspirin": 5.0, "Antibiotics": 15.0, "Cough Syrup": 8.0}

# --- Hardcoded Patient Data Configurations ---
# Change these values or create combinations to test different rules.
patient_data = {
    "name": "John Doe",
    "age": 68,                       # Senior Citizen if age >= 60
    "doctor": "Dr. Smith",
    "department": "Cardiology",
    "appointment_type": "Follow-up", # Types: "Standard", "Emergency", "Follow-up"
    "duration_hours": 1.5,           # Consultation duration
    "lab_tests": ["Blood Test", "X-Ray"],
    "medicines": ["Aspirin", "Antibiotics"],
    "has_insurance": True,
    "insurance_provider": "HealthCare Inc."
}

# --- Calculation Logic ---

print("--- Processing Patient Billing ---")

# 1. Calculate Consultation Fee based on Appointment Type Rules
consultation_fee = patient_data["duration_hours"] * BASE_CONSULTATION_RATE

if patient_data["appointment_type"] == "Emergency":
    consultation_fee += 100.0  # Extra emergency rush fee
    print("Rule Applied: Emergency Patient (+ $100.00)")
elif patient_data["appointment_type"] == "Follow-up":
    consultation_fee = consultation_fee * 0.50  # 50% discount for follow-ups
    print("Rule Applied: Follow-up Consultation (50% discount on fee)")

# 2. Calculate Lab Charges
lab_charges = 0.0
for test in patient_data["lab_tests"]:
    lab_charges += LAB_TEST_PRICES.get(test, 0.0)

# 3. Calculate Medicine Charges
medicine_charges = 0.0
for med in patient_data["medicines"]:
    medicine_charges += MEDICINE_PRICES.get(med, 0.0)

# Calculate initial gross subtotal
subtotal = consultation_fee + lab_charges + medicine_charges

# 4. Calculate Insurance Coverage
insurance_coverage = 0.0
if patient_data["has_insurance"]:
    # Insurance covers 80% of costs up to a maximum limit
    insurance_coverage = subtotal * 0.80
    print(f"Rule Applied: Insurance Patient (80% coverage covered by {patient_data['insurance_provider']})")

# 5. Apply Senior Citizen Rule
senior_discount = 0.0
if patient_data["age"] >= 60:
    # Senior citizens get 15% discount on out-of-pocket balance
    remaining_balance = subtotal - insurance_coverage
    senior_discount = remaining_balance * 0.15
    print("Rule Applied: Senior Citizen (15% additional discount on remaining balance)")

# 6. Calculate Final Patient Payable Amount
patient_payable = subtotal - insurance_coverage - senior_discount


# --- Final Invoice Summary Output ---
print("\n==========================================")
print("             HOSPITAL INVOICE             ")
print("==========================================")
print(f"Patient Name:          {patient_data['name']}")
print(f"Age / Doctor:          {patient_data['age']} yrs | {patient_data['doctor']}")
print(f"Department / Type:     {patient_data['department']} | {patient_data['appointment_type']}")
print("------------------------------------------")
print(f"Consultation Fee:      ${consultation_fee:.2f}")
print(f"Lab Charges:           ${lab_charges:.2f}")
print(f"Medicine Charges:      ${medicine_charges:.2f}")
print("------------------------------------------")
print(f"Gross Subtotal:        ${subtotal:.2f}")
print(f"Insurance Coverage:   -${insurance_coverage:.2f}")
print(f"Senior Discount:      -${senior_discount:.2f}")
print("------------------------------------------")
print(f"Patient Payable Total: ${patient_payable:.2f}")
print("==========================================")
