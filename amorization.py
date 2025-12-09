"""
amortization.py

Standalone version (for Member 2):
- Generates amortization schedule month-by-month
- Uses pandas DataFrame
- Contains temporary internal formulas so it runs without other files
- Later, replace formulas with imports from loan_calculations.py
"""

import pandas as pd


# TEMPORARY FORMULAS (until Member 1 completes their file)

def monthly_payment(P, annual_rate, n):
    """
    Standard loan payment formula.
    P = principal
    annual_rate = e.g., 0.05 for 5%
    n = number of months
    """
    r = annual_rate / 12  # monthly interest rate
    if r == 0:
        return P / n
    return P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def interest_for_month(balance, annual_rate):
    """Interest for current month."""
    return balance * (annual_rate / 12)


def principal_for_month(payment, interest):
    """Principal = payment - interest."""
    return payment - interest


def remaining_balance(balance, principal_paid):
    """Remaining balance after principal payment."""
    return balance - principal_paid


# MAIN AMORTIZATION FUNCTION


def generate_amortization_schedule(principal, annual_rate, months):
    """
    Generates a pandas DataFrame for amortization schedule.
    """

    payment = monthly_payment(principal, annual_rate, months)

    data = []
    balance = principal

    for month in range(1, months + 1):
        interest = interest_for_month(balance, annual_rate)
        principal_paid = principal_for_month(payment, interest)
        new_balance = remaining_balance(balance, principal_paid)

        # Rounded values for output clarity
        payment_r = round(payment, 2)
        interest_r = round(interest, 2)
        principal_r = round(principal_paid, 2)
        balance_r = round(max(new_balance, 0), 2)  # avoid negative balance

        data.append([month, payment_r, interest_r, principal_r, balance_r])

        balance = new_balance

    df = pd.DataFrame(data, columns=[
        "Month", "Payment", "Interest", "Principal", "Balance"
    ])

    return df


def export_to_csv(df, filename="amortization.csv"):
    """
    Saves amortization table to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"Saved amortization schedule to {filename}")


# Debug Example (optional)
if __name__ == "__main__":
    df = generate_amortization_schedule(200000, 0.05, 360)
    print(df.head())
    export_to_csv(df)
