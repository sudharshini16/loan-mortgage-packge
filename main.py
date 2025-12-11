"""
Features:
- Main menu
- Collect and validate user input
- Run calculations and amortization
- Save CSV
- Optional plots
"""

from __future__ import annotations

import inspect
from typing import Optional, Tuple

from amortization import export_to_csv, generate_amortization_schedule
from loan_calculations import (
    calculate_monthly_payment,
    calculate_remaining_balance,
    calculate_total_cost,
    calculate_total_interest,
    validate_loan_inputs,
)
from visualizations import (
    plot_balance_over_time,
    plot_cumulative_interest,
    plot_interest_vs_principal,
)

# Simple preset scenarios for quick demos
PROFILES = [
    ("Starter Home", 300000, 6.0, 30),
    ("Car Loan", 25000, 5.5, 5),
    ("Student Refi", 60000, 4.2, 10),
    ("Aggressive Paydown", 180000, 3.9, 15),
]

def prompt_number(prompt_text: str, allow_zero: bool = False) -> float:
    """Prompt for a numeric value with basic validation."""
    while True:
        raw = input(prompt_text).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if allow_zero:
            if value < 0:
                print("Value cannot be negative.")
                continue
        else:
            if value <= 0:
                print("Value must be greater than zero.")
                continue

        return value


def collect_loan_inputs():
    """Collect principal, rate (percent), and term in years."""
    print("\nEnter loan parameters (interest rate in PERCENT, e.g. 5 for 5%).")
    principal = prompt_number("  Loan principal ($): ")
    annual_rate = prompt_number("  Annual interest rate (%): ", allow_zero=True)
    years = prompt_number("  Loan term (years): ")
    return principal, annual_rate, years


def select_profile() -> Optional[Tuple[float, float, float]]:
    """Let the user pick a preset profile."""
    print("\nPreset Profiles")
    print("-" * 50)
    for idx, (name, principal, rate, years) in enumerate(PROFILES, start=1):
        print(f"{idx}) {name:<18} ${principal:>10,.0f} | {rate:>4.2f}% | {years} yrs")
    print("0) Back")

    choice = input("Select a profile number: ").strip()
    if choice == "0" or choice.lower() == "b":
        return None
    try:
        index = int(choice) - 1
        if 0 <= index < len(PROFILES):
            _, principal, rate, years = PROFILES[index]
            print(f"Using profile: {PROFILES[index][0]}")
            return float(principal), float(rate), float(years)
        print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")
    return None


def print_summary(principal: float, annual_rate: float, years: float):
    """Compute and display summary metrics."""
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    total_interest = calculate_total_interest(principal, annual_rate, years)
    total_cost = calculate_total_cost(principal, annual_rate, years)
    # Example balance after 5 years (or full term if shorter)
    payments_for_5_years = min(int(round(years * 12)), 60)
    balance_after_5_years = calculate_remaining_balance(
        principal, annual_rate, years, payments_made=payments_for_5_years
    )

    print("\n=== Loan Summary ===")
    print(f"Principal:            ${principal:,.2f}")
    print(f"Annual rate:           {annual_rate:.2f}%")
    print(f"Term:                  {years} years")
    print(f"Monthly payment:      ${monthly_payment:,.2f}")
    print(f"Total interest:       ${total_interest:,.2f}")
    print(f"Total cost:           ${total_cost:,.2f}")
    print(f"Balance after 5 years:${balance_after_5_years:,.2f}")


def run_analysis(preset: Optional[Tuple[float, float, float]] = None):
    """Execute full workflow: inputs -> summary -> schedule -> CSV -> plots."""
    if preset is None:
        principal, annual_rate, years = collect_loan_inputs()
    else:
        principal, annual_rate, years = preset

    try:
        validate_loan_inputs(principal, annual_rate, years)
    except (TypeError, ValueError) as exc:
        print(f"\nInput error: {exc}")
        return

    try:
        print_summary(principal, annual_rate, years)

        # Be tolerant to either amortization API shape (years or months).
        sig = inspect.signature(generate_amortization_schedule)
        params = list(sig.parameters)
        months_int = int(round(years * 12))
        if "years" in params:
            schedule_df = generate_amortization_schedule(principal, annual_rate, years)
        elif "months" in params:
            # Legacy version expected annual_rate as a decimal (e.g., 0.05) and months count.
            schedule_df = generate_amortization_schedule(principal, annual_rate / 100.0, months_int)
        else:
            schedule_df = generate_amortization_schedule(principal, annual_rate, years)

        default_csv = "amortization.csv"
        csv_name = input(f"\nEnter CSV filename [{default_csv}]: ").strip() or default_csv
        export_to_csv(schedule_df, csv_name)

        make_plots = input("Generate plots? [y/N]: ").strip().lower()
        if make_plots == "y":
            plot_balance_over_time(schedule_df, "balance_over_time.png")
            plot_interest_vs_principal(schedule_df, "interest_vs_principal.png")
            plot_cumulative_interest(schedule_df, "cumulative_interest.png")
            print("Plots saved (see .png files).")
    except (TypeError, ValueError) as exc:
        print(f"\nCalculation error: {exc}")
    except Exception as exc:
        print(f"\nUnexpected error: {exc}")

    print("\nDone. Select another option or exit.")


def main():
    """CLI menu loop."""
    print("=" * 60)
    print("        Loan & Mortgage Toolkit")
    print("=" * 60)
    print("Calculates payments, builds amortization schedules, and plots results.\n")

    while True:
        try:
            print("-" * 60)
            print("Menu:")
            print("  1) Custom loan analysis")
            print("  2) Use a preset profile")
            print("  3) Exit")
            choice = input("Select an option: ").strip()

            if choice == "1":
                run_analysis()
            elif choice == "2":
                profile = select_profile()
                if profile:
                    run_analysis(profile)
            elif choice == "3" or choice.lower() == "q":
                print("Goodbye!")
                break
            else:
                print("Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()

