# Travel Activity Optimizer

A Python-based optimization project that recommends travel activities while maximizing enjoyment within a fixed budget and time limit. It uses **linear programming** and **mixed-integer optimization** with SciPy.

## Features

- Maximizes total enjoyment points for selected activities.
- Considers budget and available time constraints.
- Uses `scipy.optimize.linprog` for linear programming.
- Uses `scipy.optimize.milp` to select whole activities instead of fractional activities.
- Displays the recommended itinerary, total cost, time required, and enjoyment score.
- Allows users to customize the budget and time limit.

## Technologies Used

- Python
- NumPy
- SciPy
- Linear Programming (LP)
- Mixed-Integer Linear Programming (MILP)

## Project Structure

```text
travel-activity-optimizer/
├── optimizer.py
├── README.md
├── requirements.txt
├── .gitignore
└── verification.txt
```

## Installation

### Prerequisites

- Python 3.13 or a compatible Python version
- pip package installer

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd travel-activity-optimizer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 3. Run the program

```bash
py optimizer.py
```

## Example

The program uses sample activities with different costs, durations, and enjoyment scores.

**Constraints:**
- Budget: ₹1,800
- Available time: 7 hours

**Recommended itinerary:**

| Activity | Cost | Duration | Enjoyment |
|---|---:|---:|---:|
| Museum visit | ₹500 | 2 hours | 7 |
| City walking tour | ₹300 | 3 hours | 8 |
| Local food experience | ₹700 | 2 hours | 9 |
| **Total** | **₹1,500** | **7 hours** | **24 points** |

The recommended itinerary stays within the budget and uses the available time efficiently.

The linear programming relaxation reports a maximum enjoyment score of approximately 27.33 when fractional activity selections are allowed. The mixed-integer optimization selects whole activities and produces a practical itinerary with 24 enjoyment points.

## How It Works

1. Each activity is represented by its cost, duration, and enjoyment score.
2. The linear programming model maximizes total enjoyment subject to budget and time constraints.
3. The LP relaxation allows fractional activity selections for comparison.
4. The mixed-integer model restricts activity selections to 0 or 1, ensuring each activity is either selected or not selected.
5. The program displays the resulting itinerary and its totals.

## Customization

You can modify the budget and time limit in `optimizer.py`.

For example:

```python
BUDGET_INR = 1800
TIME_LIMIT_HOURS = 7
```

Change these values to explore different travel-planning scenarios.

## Learning Outcomes

This project demonstrates:

- Python programming and numerical optimization.
- Formulating objective functions and constraints.
- Applying linear programming with SciPy.
- Using mixed-integer optimization for practical selection problems.
- Validating results against budget and time limits.

## Limitations

- Activities, prices, durations, and enjoyment scores are illustrative sample data.
- The project does not retrieve live prices, opening hours, bookings, or real-time travel information.
- Enjoyment scores are example values and should be adjusted to reflect individual preferences.

## Future Improvements

- Allow users to enter custom activities.
- Add destination-specific activity data.
- Include travel time between activities.
- Build a web interface using Flask or Django.
- Integrate external APIs for real-time activity and location information.

## License

This project is available for educational and portfolio purposes. Add a license file if you intend to distribute it under a specific open-source license.
