import pandas as pd
import math


# Load goal cost dataset

goal_data = pd.read_csv(
    "data/city_goal_costs.csv"
)


INFLATION_RATE = 0.06


# Expected investment return assumption

EXPECTED_RETURN = 0.10


def get_current_goal_cost(city, goal):

    city_data = goal_data[
        goal_data["City"].str.lower()
        ==
        city.lower()
    ]


    if city_data.empty:

        return None


    if goal == "Marriage":

        return city_data[
            "Marriage_Cost_Current"
        ].mean()


    elif goal == "Car":

        return city_data[
            "Car_Cost_Current"
        ].mean()


    elif goal == "Home":

        return city_data[
            "Home_Cost_Current"
        ].mean()


    return None


def calculate_future_cost(
    current_cost,
    years
):

    future_cost = current_cost * (
        (1 + INFLATION_RATE) ** years
    )

    return round(
        future_cost,
        2
    )


def calculate_monthly_investment(
    future_cost,
    years
):

    months = years * 12

    monthly_rate = EXPECTED_RETURN / 12


    if monthly_rate == 0:

        return future_cost / months


    sip = future_cost * monthly_rate / (
        ((1 + monthly_rate) ** months) - 1
    )


    return round(
        sip,
        2
    )


def get_investment_category(years):

    if years <= 3:

        return "Short-term: Lower-volatility / Capital-preservation-oriented"

    elif years <= 7:

        return "Medium-term: Diversified balanced category"

    else:

        return "Long-term: Diversified growth-oriented category"


def analyze_feasibility(
    required,
    capacity
):

    difference = capacity - required


    if capacity >= required:

        status = "Achievable"

    elif capacity >= required * 0.70:

        status = "Challenging"

    else:

        status = "Highly Challenging"


    return {

        "status": status,

        "difference": round(
            difference,
            2
        )

    }
