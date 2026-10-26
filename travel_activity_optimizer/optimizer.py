
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def get_number(prompt, minimum, allow_zero=False):
    """Read and validate a positive number from the user."""
    while True:
        try:
            value = float(input(prompt))

            if not np.isfinite(value):
                print("Please enter a finite number.")
                continue

            if allow_zero and value == 0:
                return value

            if value < minimum:
                print(f"Please enter a number greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_integer(prompt, minimum, maximum):
    """Read and validate an integer."""
    while True:
        try:
            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Enter a whole number between {minimum} and {maximum}.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_activities():
    """Collect travel activities from the user."""
    activities = []

    count = get_integer(
        "\nHow many activities do you want to consider? (1-100): ",
        1,
        100,
    )

    print("\nEnter the details for each activity.")

    for i in range(count):
        print(f"\nActivity {i + 1}")

        while True:
            name = input("Activity name: ").strip()

            if name:
                break

            print("Activity name cannot be empty.")

        cost = get_number("Cost in INR: ", 0, allow_zero=True)
        hours = get_number("Duration in hours: ", 0.01)
        enjoyment = get_number("Enjoyment score: ", 0.01)

        activities.append({
            "name": name,
            "cost": cost,
            "hours": hours,
            "enjoyment": enjoyment,
        })

    return activities


def optimize_activities(activities, budget, time_limit):
    """Solve both the LP relaxation and whole-activity problem."""
    costs = np.array([a["cost"] for a in activities], dtype=float)
    durations = np.array([a["hours"] for a in activities], dtype=float)
    enjoyment = np.array([a["enjoyment"] for a in activities], dtype=float)

    # Each activity is represented by a decision variable.
    # 0 means not selected; 1 means selected.
    constraints_matrix = np.vstack([costs, durations])
    limits = np.array([budget, time_limit], dtype=float)

    # LP relaxation: variables can be fractional between 0 and 1.
    lp_result = linprog(
        c=-enjoyment,  # Negate scores to maximize enjoyment.
        A_ub=constraints_matrix,
        b_ub=limits,
        bounds=[(0, 1)] * len(activities),
        method="highs",
    )

    # Mixed-integer optimization: each activity must be 0 or 1.
    milp_result = milp(
        c=-enjoyment,
        integrality=np.ones(len(activities), dtype=int),
        bounds=Bounds(
            np.zeros(len(activities)),
            np.ones(len(activities)),
        ),
        constraints=LinearConstraint(
            constraints_matrix,
            lb=np.array([-np.inf, -np.inf]),
            ub=limits,
        ),
    )

    if not milp_result.success or milp_result.x is None:
        print("\nOptimization could not find a solution.")
        print(milp_result.message)
        return

    # Round binary decisions only, not arbitrary fractional solutions.
    selected = [
        i for i, value in enumerate(milp_result.x)
        if value > 0.5
    ]

    print("\n" + "=" * 48)
    print("       TRAVEL ACTIVITY OPTIMIZER")
    print("=" * 48)
    print(f"Budget: INR {budget:.2f}")
    print(f"Available time: {time_limit:.2f} hours")

    if lp_result.success:
        print(
            "\nLP relaxation maximum enjoyment "
            f"(fractional activities allowed): {-lp_result.fun:.2f}"
        )
    else:
        print("\nLP relaxation could not be solved:", lp_result.message)

    print("\nRECOMMENDED ITINERARY")

    if not selected:
        print("No activities selected within the given constraints.")
        total_cost = 0.0
        total_hours = 0.0
        total_enjoyment = 0.0
    else:
        for i in selected:
            activity = activities[i]
            print(
                f"- {activity['name']}: "
                f"INR {activity['cost']:.2f}, "
                f"{activity['hours']:.2f} hours, "
                f"{activity['enjoyment']:.2f} enjoyment points"
            )

        total_cost = sum(costs[i] for i in selected)
        total_hours = sum(durations[i] for i in selected)
        total_enjoyment = sum(enjoyment[i] for i in selected)

    print("\nTOTALS")
    print(f"Activities selected: {len(selected)}")
    print(f"Total cost: INR {total_cost:.2f} / INR {budget:.2f}")
    print(f"Total time: {total_hours:.2f} / {time_limit:.2f} hours")
    print(f"Total enjoyment: {total_enjoyment:.2f} points")
    print("=" * 48)


def main():
    print("=" * 48)
    print("Welcome to the Travel Activity Optimizer!")
    print("Choose activities within your budget and time.")
    print("=" * 48)

    budget = get_number(
        "\nEnter your total budget in INR: ",
        0,
        allow_zero=True,
    )

    time_limit = get_number(
        "Enter your available time in hours: ",
        0.01,
    )

    activities = get_activities()
    optimize_activities(activities, budget, time_limit)


if __name__ == "__main__":
    main()
