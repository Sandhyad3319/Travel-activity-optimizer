"""
Travel Activity Optimizer
Select activities that maximize total enjoyment under budget and time limits.

This is a 0/1 integer selection problem solved with scipy.optimize.milp.
The user specifically asked to practice scipy.optimize.linprog, so a continuous
LP relaxation using linprog is also included for comparison. The LP relaxation
can return fractional activity selections; the integer solution is the practical
itinerary.
"""
import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint


ACTIVITIES = [
    # name, cost (INR), duration (hours), enjoyment points
    ("Museum visit", 500, 2, 7),
    ("City walking tour", 300, 3, 8),
    ("Local food experience", 700, 2, 9),
    ("Botanical garden", 250, 2, 5),
    ("Day trip to nearby town", 1200, 5, 10),
    ("Art gallery", 400, 1, 6),
]

BUDGET_INR = 1800
TIME_LIMIT_HOURS = 7


def solve_lp_relaxation():
    """Solve the linear programming relaxation with scipy.optimize.linprog."""
    costs = np.array([a[1] for a in ACTIVITIES], dtype=float)
    durations = np.array([a[2] for a in ACTIVITIES], dtype=float)
    enjoyment = np.array([a[3] for a in ACTIVITIES], dtype=float)

    # linprog minimizes, so negate enjoyment to maximize it.
    result = linprog(
        c=-enjoyment,
        A_ub=np.vstack([costs, durations]),
        b_ub=np.array([BUDGET_INR, TIME_LIMIT_HOURS], dtype=float),
        bounds=[(0, 1)] * len(ACTIVITIES),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"LP solver failed: {result.message}")
    return result


def solve_integer_itinerary():
    """Solve the realistic 0/1 activity-selection problem."""
    costs = np.array([a[1] for a in ACTIVITIES], dtype=float)
    durations = np.array([a[2] for a in ACTIVITIES], dtype=float)
    enjoyment = np.array([a[3] for a in ACTIVITIES], dtype=float)

    result = milp(
        c=-enjoyment,
        integrality=np.ones(len(ACTIVITIES)),
        bounds=Bounds(np.zeros(len(ACTIVITIES)), np.ones(len(ACTIVITIES))),
        constraints=LinearConstraint(
            np.vstack([costs, durations]),
            lb=np.array([-np.inf, -np.inf]),
            ub=np.array([BUDGET_INR, TIME_LIMIT_HOURS]),
        ),
        options={"disp": False},
    )
    if not result.success:
        raise RuntimeError(f"Integer solver failed: {result.message}")
    return result


def main():
    lp_result = solve_lp_relaxation()
    integer_result = solve_integer_itinerary()

    print("TRAVEL ACTIVITY OPTIMIZER")
    print(f"Budget: ₹{BUDGET_INR}; time limit: {TIME_LIMIT_HOURS} hours")
    print(f"LP relaxation maximum enjoyment (fractional allowed): {-lp_result.fun:.2f}")
    print("\nRecommended itinerary (whole activities only):")

    chosen = []
    total_cost = 0
    total_time = 0
    total_enjoyment = 0
    for activity, selected in zip(ACTIVITIES, integer_result.x):
        if selected > 0.5:
            name, cost, hours, points = activity
            chosen.append(name)
            total_cost += cost
            total_time += hours
            total_enjoyment += points
            print(f"- {name}: ₹{cost}, {hours} hours, {points} enjoyment points")

    print("\nTotals")
    print(f"Activities: {len(chosen)}")
    print(f"Cost: ₹{total_cost} / ₹{BUDGET_INR}")
    print(f"Time: {total_time} / {TIME_LIMIT_HOURS} hours")
    print(f"Enjoyment: {total_enjoyment} points")


if __name__ == "__main__":
    main()
