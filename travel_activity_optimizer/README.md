# Travel Activity Optimizer

A small optimization project for an AI Travel Planner. It selects activities to
maximize enjoyment while respecting a travel budget and available time.

## Problem

Each activity has a cost, duration, and enjoyment score. The optimizer must
choose activities such that:

- Total cost is at most **₹1,800**
- Total duration is at most **7 hours**
- Enjoyment score is maximized

## Methods

- `scipy.optimize.linprog` solves the **linear programming relaxation**, where
  an activity can be selected fractionally (useful for demonstrating LP).
- `scipy.optimize.milp` solves the practical **0/1 activity-selection** version,
  where each activity is either selected or not selected.

The integer version is used for the final itinerary because real activities
cannot usually be selected fractionally.

## Run locally

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python optimizer.py
```

## Example output

The exact solver output is printed in the terminal, including selected activities,
total cost, total hours, and total enjoyment points.

## Files

- `optimizer.py` — activity data and optimization code
- `requirements.txt` — dependencies

## Note

The activity costs, durations, and enjoyment scores are illustrative sample data,
not live prices or personalized recommendations.
