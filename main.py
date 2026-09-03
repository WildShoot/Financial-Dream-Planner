from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import joblib
from rag import search_knowledge

from financial_tools import (
    get_current_goal_cost,
    calculate_future_cost,
    calculate_monthly_investment,
    get_investment_category,
    analyze_feasibility
)
#API Implemetation
app = FastAPI(
    title="AI Financial Dream Planner",
    description="AI-powered financial planning system for freshers"
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Load trained salary prediction model

salary_model = joblib.load(
    "models/salary_model.pkl"
)

@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )

# INPUT MODEL FOR FINANCIAL PLANNING
class UserInput(BaseModel):

    name: str
    age: int
    city: str
    education: str
    job_role: str

    marriage_years: int
    car_years: int
    home_years: int

    saving_percentage: float



# INPUT MODEL FOR RAG QUESTION

class QuestionInput(BaseModel):

    question: str


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to AI Financial Dream Planner"
    }


# ==========================================
# FINANCIAL PLANNING API
# ==========================================

@app.post("/plan")
def create_plan(user: UserInput):


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if user.saving_percentage < 0 or user.saving_percentage > 100:

        return {
            "error": "Saving percentage must be between 0 and 100"
        }


    if (
        user.marriage_years <= 0
        or user.car_years <= 0
        or user.home_years <= 0
    ):

        return {
            "error": "Goal timelines must be greater than 0"
        }


    # --------------------------------------
    # SALARY PREDICTION
    # --------------------------------------

    salary_input = pd.DataFrame([{

        "Age": user.age,
        "City": user.city,
        "Education": user.education,
        "Job_Role": user.job_role

    }])


    predicted_salary = salary_model.predict(
        salary_input
    )[0]


    predicted_salary = round(
        float(predicted_salary),
        2
    )


    # --------------------------------------
    # INVESTMENT CAPACITY
    # --------------------------------------

    investment_capacity = (

        predicted_salary
        *
        user.saving_percentage
        /
        100

    )


    investment_capacity = round(
        investment_capacity,
        2
    )


    # --------------------------------------
    # GOALS
    # --------------------------------------

    goals = {

        "Marriage": user.marriage_years,

        "Car": user.car_years,

        "Home": user.home_years

    }


    results = {}

    total_required = 0


    # --------------------------------------
    # CALCULATE EACH GOAL
    # --------------------------------------

    for goal, years in goals.items():


        # Get current goal cost

        current_cost = get_current_goal_cost(

            user.city,

            goal

        )


        # Check if city exists

        if current_cost is None:

            return {

                "error":
                f"City '{user.city}' not found in goal cost dataset"

            }


        # Calculate future cost

        future_cost = calculate_future_cost(

            current_cost,

            years

        )


        # Calculate required monthly investment

        monthly_investment = calculate_monthly_investment(

            future_cost,

            years

        )


        # Get investment category

        category = get_investment_category(

            years

        )


        # Check feasibility

        feasibility = analyze_feasibility(

            monthly_investment,

            investment_capacity

        )


        # Store result

        results[goal] = {

            "timeline_years": years,

            "current_cost":
            round(float(current_cost), 2),

            "future_cost":
            future_cost,

            "monthly_investment_required":
            monthly_investment,

            "investment_category":
            category,

            "status":
            feasibility["status"]

        }


        # Add to total requirement

        total_required += monthly_investment


    # --------------------------------------
    # OVERALL FEASIBILITY
    # --------------------------------------

    overall = analyze_feasibility(

        total_required,

        investment_capacity

    )


    # --------------------------------------
    # FINAL RESPONSE
    # --------------------------------------

    return {

        "user_name": user.name,

        "predicted_monthly_salary":
        predicted_salary,

        "saving_percentage":
        user.saving_percentage,

        "monthly_investment_capacity":
        investment_capacity,

        "goals":
        results,

        "total_monthly_investment_required":
        round(total_required, 2),

        "monthly_surplus_or_shortfall":
        overall["difference"],

        "overall_status":
        overall["status"],

        "suggestion":
        get_suggestion(
            overall["difference"]
        )

    }


# ==========================================
# SUGGESTION FUNCTION
# ==========================================

def get_suggestion(difference):


    if difference >= 0:

        return (
            "Your current saving capacity appears sufficient "
            "for the selected financial plan."
        )


    else:

        return (

            "Your saving capacity is not sufficient. "
            "You can increase your saving percentage, "
            "increase the goal timeline, or reduce the goal amount."

        )


# ==========================================
# RAG QUESTION API
# ==========================================

@app.post("/ask")
def ask_question(data: QuestionInput):

    return search_knowledge(data.question)