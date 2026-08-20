# --- HARDCODED TEST INPUTS ---
customer_id = "CUST-9082"
age = 29
monthly_salary = 5000.0
existing_loan_amount = 12000.0
credit_score = 780
employment_type = "Salaried"
requested_loan_amount = 45000.0
loan_tenure = 36  # in months

# --- CALCULATIONS ---

# 1. Debt-to-Income (DTI) Ratio
# Assuming existing monthly debt payment is 5% of the total existing loan amount
estimated_monthly_debt = existing_loan_amount * 0.05
debt_to_income_ratio = (estimated_monthly_debt / monthly_salary) * 100

# 2. Eligible Loan Amount
# Eligibility multiplier varies based on credit score
if credit_score >= 750:
    eligible_loan_amount = monthly_salary * 50
elif credit_score >= 650:
    eligible_loan_amount = monthly_salary * 30
else:
    eligible_loan_amount = monthly_salary * 10

# 3. Interest Rate
# Base interest rate is adjusted according to the credit score
annual_interest_rate = 10.0  # Base rate 10%
if credit_score >= 750:
    annual_interest_rate -= 2.0  # 8% for excellent credit
elif credit_score >= 650:
    annual_interest_rate -= 0.5  # 9.5% for good credit
else:
    annual_interest_rate += 2.0  # 12% for poor credit

# 4. Equated Monthly Installment (EMI) Calculation
# Formula: EMI = [P x R x (1+R)^N] / [(1+R)^N - 1]
monthly_interest_rate = (annual_interest_rate / 12) / 100
if monthly_interest_rate > 0:
    emi = (requested_loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_tenure)) / (((1 + monthly_interest_rate) ** loan_tenure) - 1)
else:
    emi = requested_loan_amount / loan_tenure

# 5. Approval / Rejection Status
# Criteria: Approved if age is valid, credit score is decent, DTI is low, and requested amount is within limit
status = "Rejected"
if age >= 21 and age <= 65 and credit_score >= 600 and debt_to_income_ratio <= 50.0 and requested_loan_amount <= eligible_loan_amount:
    status = "Approved"

# --- OUTPUT GENERATION ---
print("\n=============================================")
print("          LOAN PROCESSING REPORT             ")
print("=============================================")
print(f"Customer ID: {customer_id}")
print(f"Debt-to-Income (DTI) Ratio: {debt_to_income_ratio:.2f}%")
print(f"Maximum Eligible Loan Amount: ${eligible_loan_amount:.2f}")
print(f"Offered Annual Interest Rate: {annual_interest_rate:.2f}%")
print(f"Estimated Monthly EMI: ${emi:.2f}")
print(f"Application Status: {status}")
print("=============================================")

