import math

# --- CORE FUNCTION TO TEST ---
def process_loan(customer_id, age, monthly_salary, existing_loan, credit_score, employment_type, requested_loan, loan_tenure):
    # Exception Handling: Validate data types
    if not isinstance(age, (int, float)) or not isinstance(monthly_salary, (int, float)) or not isinstance(credit_score, (int, float)):
        raise TypeError("Invalid data types provided.")
        
    # Invalid Input Handling
    if age < 0 or monthly_salary <= 0 or existing_loan < 0 or requested_loan <= 0 or loan_tenure <= 0:
        return "Rejected (Invalid Negative/Zero Values)"
    if credit_score < 300 or credit_score > 850:
        return "Rejected (Credit Score Out of Range)"

    # 1. Debt-to-Income (DTI) Ratio
    estimated_monthly_debt = existing_loan * 0.05
    debt_to_income_ratio = (estimated_monthly_debt / monthly_salary) * 100

    # 2. Eligible Loan Amount Limit
    if credit_score >= 750:
        eligible_loan_amount = monthly_salary * 50
    elif credit_score >= 650:
        eligible_loan_amount = monthly_salary * 30
    else:
        eligible_loan_amount = monthly_salary * 10

    # 3. Interest Rate Determination
    annual_interest_rate = 10.0
    if credit_score >= 750:
        annual_interest_rate -= 2.0
    elif credit_score >= 650:
        annual_interest_rate -= 0.5
    else:
        annual_interest_rate += 2.0

    # 4. EMI Calculation
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    emi = (requested_loan * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_tenure)) / (((1 + monthly_interest_rate) ** loan_tenure) - 1)

    # 5. Final Status Verification
    if age < 21 or age > 65:
        return f"Rejected (Age Limit Violation) | EMI: ${emi:.2f}"
    if debt_to_income_ratio > 50.0:
        return f"Rejected (High DTI Ratio: {debt_to_income_ratio:.1f}%) | EMI: ${emi:.2f}"
    if requested_loan > eligible_loan_amount:
        return f"Rejected (Exceeded Eligible Limit of ${eligible_loan_amount:.2f}) | EMI: ${emi:.2f}"
    
    return f"Approved | EMI: ${emi:.2f}"


# --- QA AUTOMATED TEST SUITE ---
print("==================================================================")
print("               LOAN PROCESSING QA TEST SUITE                      ")
print("==================================================================")

# Scenario 1: Minimum/Maximum Age
print(f"Test 1a (Age under 21):   {process_loan('C1', 19, 5000, 2000, 750, 'Salaried', 20000, 36)}")
print(f"Test 1b (Age over 65):    {process_loan('C2', 68, 5000, 2000, 750, 'Salaried', 20000, 36)}")

# Scenario 2: Invalid Salary
print(f"Test 2 (Zero/Negative Salary): {process_loan('C3', 30, 0, 2000, 700, 'Salaried', 10000, 12)}")

# Scenario 3: Poor Credit Score
print(f"Test 3 (Low Credit Score): {process_loan('C4', 35, 4000, 0, 450, 'Salaried', 15000, 24)}")

# Scenario 4 & 5: Existing Loan / High DTI Ratio
print(f"Test 4/5 (High DTI > 50%): {process_loan('C5', 40, 3000, 40000, 720, 'Salaried', 10000, 24)}")

# Scenario 6: Different Employment Categories
print(f"Test 6a (Salaried Case):   {process_loan('C6', 28, 6000, 5000, 760, 'Salaried', 50000, 48)}")
print(f"Test 6b (Self-Employed):   {process_loan('C7', 32, 6000, 5000, 760, 'Self-Employed', 50000, 48)}")

# Scenario 7: Boundary Loan Amounts
print(f"Test 7 (Exceed Eligible Max): {process_loan('C8', 45, 2000, 0, 800, 'Salaried', 150000, 36)}")

# Scenario 8: EMI Calculation Accuracy Verification
print(f"Test 8 (Verify EMI Math):  {process_loan('C9', 30, 5000, 0, 800, 'Salaried', 10000, 12)}")

# Scenario 9: Invalid Input Handling
print(f"Test 9 (Negative Loan Request): {process_loan('C10', 25, 4000, 1000, 700, 'Salaried', -5000, 12)}")

# Scenario 10: Exception Handling
print("Test 10 (Type Exception Handling): ", end="")
try:
    process_loan('C11', "Thirty", 5000, 0, 700, 'Salaried', 10000, 12)
except TypeError as e:
    print(f"Caught Expected Exception -> {e}")

print("==================================================================")
