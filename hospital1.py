# --- Base Rates Configuration ---
BASE_RATE = 50.0
LAB_PRICES = {"Blood Test": 20.0, "X-Ray": 50.0}
MED_PRICES = {"Aspirin": 5.0, "Antibiotics": 15.0}

def calculate_patient_bill(patient):
    # Calculate initial consultation fee
    consultation_fee = patient["duration"] * BASE_RATE
    
    # Rule 1: Emergency Patient (+ $100 fee)
    if patient["type"] == "Emergency":
        consultation_fee += 100.0
    # Rule 2: Follow-up Consultation (50% discount)
    elif patient["type"] == "Follow-up":
        consultation_fee *= 0.5

    # Sum up lab charges
    lab_charges = sum(LAB_PRICES.get(test, 0.0) for test in patient["labs"])
    
    # Sum up medicine charges
    medicine_charges = sum(MED_PRICES.get(med, 0.0) for med in patient["meds"])
    
    # Gross total bill before insurance and age discounts
    gross_total = consultation_fee + lab_charges + medicine_charges
    
    # Rule 3: Insurance Coverage (Covers 80% if patient has insurance)
    insurance_coverage = gross_total * 0.80 if patient["insurance"] else 0.0
    
    # Balance left after insurance
    remaining = gross_total - insurance_coverage
    
    # Rule 4: Senior Citizen (15% discount on remaining balance if age >= 60)
    senior_discount = remaining * 0.15 if patient["age"] >= 60 else 0.0
    
    # Final amount the patient owes
    final_payable = remaining - senior_discount
    
    return {
        "consultation": consultation_fee,
        "labs": lab_charges,
        "meds": medicine_charges,
        "insurance_covered": insurance_coverage,
        "senior_discount": senior_discount,
        "final": final_payable
    }

# --- Multiple QA Test Scenarios ---
scenarios = [
    {
        "desc": "Scenario 1: Standard Patient (No special rules)",
        "age": 30, "type": "Standard", "duration": 1, 
        "labs": ["Blood Test"], "meds": ["Aspirin"], "insurance": False
    },
    {
        "desc": "Scenario 2: Emergency Patient (+ $100 fee)",
        "age": 25, "type": "Emergency", "duration": 1, 
        "labs": ["X-Ray"], "meds": ["Antibiotics"], "insurance": False
    },
    {
        "desc": "Scenario 3: Senior Citizen (15% discount)",
        "age": 65, "type": "Standard", "duration": 1, 
        "labs": ["Blood Test"], "meds": ["Aspirin"], "insurance": False
    },
    {
        "desc": "Scenario 4: Insurance Patient (80% covered)",
        "age": 40, "type": "Standard", "duration": 2, 
        "labs": ["Blood Test", "X-Ray"], "meds": ["Antibiotics"], "insurance": True
    },
    {
        "desc": "Scenario 5: Follow-up Consultation (50% fee discount)",
        "age": 35, "type": "Follow-up", "duration": 1, 
        "labs": [], "meds": ["Aspirin"], "insurance": False
    },
    {
        "desc": "Scenario 6: Senior Citizen + Insurance Combo",
        "age": 70, "type": "Standard", "duration": 1, 
        "labs": ["Blood Test"], "meds": ["Antibiotics"], "insurance": True
    }
]

# --- Execute and Verify Calculations ---
print("=========================================================================")
print("                   HOSPITAL MANAGEMENT SYSTEM - QA REPORT               ")
print("=========================================================================\n")

for item in scenarios:
    bill = calculate_patient_bill(item)
    print(f"📌 {item['desc']}")
    print(f"   -> Consultation: ${bill['consultation']:.2f} | Labs: ${bill['labs']:.2f} | Meds: ${bill['meds']:.2f}")
    print(f"   -> Insurance Paid: -${bill['insurance_covered']:.2f} | Senior Discount: -${bill['senior_discount']:.2f}")
    print(f"   => FINAL PAYABLE AMOUNT: ${bill['final']:.2f}\n")

print("=========================================================================")
