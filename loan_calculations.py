"""
loan_calculations.py

Core loan and mortgage calculation utilities.

This module provides functions to:
- Validate loan inputs
- Compute monthly payment for a fixed-rate loan
- Compute remaining balance after k payments
- Compute total interest paid
- Compute total cost (principal + interest)

Assumptions:
- Fixed-rate loan
- Payments are monthly
- annual_interest_rate is given in PERCENT (e.g. 5.0 means 5%)
"""

def validate_loan_inputs(principal, annual_interest_rate, years):
    """
    Validate basic loan inputs.

    Parameters
    ----------
    principal : float
        Amount borrowed. Must be > 0.
    annual_interest_rate : float
        Annual interest rate in percent. Must be >= 0.
    years : float
        Loan term in years. Must be > 0.

    Raises
    ------
    TypeError
        If types are not int or float.
    ValueError
        If values are outside allowed ranges.
    """
    for name, value in (
        ("principal", principal),
        ("annual_interest_rate", annual_interest_rate),
        ("years", years),
    ):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(value).__name__}")

    if principal <= 0:
        raise ValueError("principal must be greater than 0")

    if annual_interest_rate < 0:
        raise ValueError("annual_interest_rate cannot be negative")

    if years <= 0:
        raise ValueError("years must be greater than 0")


def calculate_monthly_payment(principal, annual_interest_rate, years):
    """
    Calculate the fixed monthly payment for a loan.

    Parameters
    ----------
    principal : float
        Amount borrowed. Must be > 0.
    annual_interest_rate : float
        Annual interest rate in percent. Must be >= 0.
        Example: 5.0 means 5% per year.
    years : float
        Loan term in years. Must be > 0.

    Returns
    -------
    float
        Monthly payment amount.

    Notes
    -----
    If monthly rate r > 0:

        M = P * r / (1 - (1 + r)^(-n))

    where:
        P = principal
        r = monthly interest rate
        n = total number of monthly payments

    If r = 0:

        M = P / n
    """
    validate_loan_inputs(principal, annual_interest_rate, years)

    # total number of monthly payments
    months = int(round(years * 12))
    if months <= 0:
        raise ValueError("Loan term must result in at least 1 month of payments")

    monthly_rate = (annual_interest_rate / 100.0) / 12.0

    if monthly_rate == 0:
        # No interest
        return principal / months

    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-months))
    return payment


def calculate_remaining_balance(principal, annual_interest_rate, years, payments_made):
    """
    Calculate remaining balance after a certain number of monthly payments.

    Parameters
    ----------
    principal : float
        Amount borrowed. Must be > 0.
    annual_interest_rate : float
        Annual interest rate in percent. Must be >= 0.
    years : float
        Loan term in years. Must be > 0.
    payments_made : int
        Number of monthly payments already made. Must be >= 0.

    Returns
    -------
    float
        Remaining balance (never negative).
    """
    validate_loan_inputs(principal, annual_interest_rate, years)

    if not isinstance(payments_made, int):
        raise TypeError("payments_made must be an integer")
    if payments_made < 0:
        raise ValueError("payments_made cannot be negative")

    months = int(round(years * 12))
    if months <= 0:
        raise ValueError("Loan term must result in at least 1 month of payments")

    # If loan is fully paid or more, balance is zero
    if payments_made >= months:
        return 0.0

    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, years)
    monthly_rate = (annual_interest_rate / 100.0) / 12.0

    if monthly_rate == 0:
        # No interest: principal is reduced linearly
        remaining = principal - monthly_payment * payments_made
        return max(remaining, 0.0)

    k = payments_made
    factor = (1 + monthly_rate) ** k

    # Balance formula:
    # B_k = P * (1 + r)^k - M * ((1 + r)^k - 1) / r
    remaining = principal * factor - monthly_payment * (factor - 1) / monthly_rate
    return max(remaining, 0.0)


def calculate_total_interest(principal, annual_interest_rate, years):
    """
    Calculate total interest paid over the full life of the loan.

    Parameters
    ----------
    principal : float
        Amount borrowed. Must be > 0.
    annual_interest_rate : float
        Annual interest rate in percent. Must be >= 0.
    years : float
        Loan term in years. Must be > 0.

    Returns
    -------
    float
        Total interest paid.
    """
    validate_loan_inputs(principal, annual_interest_rate, years)

    months = int(round(years * 12))
    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, years)
    total_paid = monthly_payment * months
    total_interest = total_paid - principal
    return total_interest


def calculate_total_cost(principal, annual_interest_rate, years):
    """
    Calculate total cost of the loan (principal + interest).

    Parameters
    ----------
    principal : float
        Amount borrowed. Must be > 0.
    annual_interest_rate : float
        Annual interest rate in percent. Must be >= 0.
    years : float
        Loan term in years. Must be > 0.

    Returns
    -------
    float
        Total amount paid = principal + interest.
    """
    validate_loan_inputs(principal, annual_interest_rate, years)
    total_interest = calculate_total_interest(principal, annual_interest_rate, years)
    return principal + total_interest


# >>> THIS PART IS WHAT PRINTS OUTPUT WHEN YOU RUN THE FILE <<<
if __name__ == "__main__":
    # Example loan parameters
    principal = 300000        # $300,000
    annual_rate = 5.0         # 5% interest
    years = 30                # 30-year mortgage

    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    total_interest = calculate_total_interest(principal, annual_rate, years)
    total_cost = calculate_total_cost(principal, annual_rate, years)
    balance_after_5_years = calculate_remaining_balance(
        principal, annual_rate, years, payments_made=5*12
    )

    print("=== Loan Summary ===")
    print(f"Principal:        ${principal:,.2f}")
    print(f"Annual rate:       {annual_rate:.2f}%")
    print(f"Term:              {years} years")
    print()
    print(f"Monthly payment:  ${monthly_payment:,.2f}")
    print(f"Total interest:   ${total_interest:,.2f}")
    print(f"Total cost:       ${total_cost:,.2f}")
    print(f"Balance after 5 years: ${balance_after_5_years:,.2f}")
