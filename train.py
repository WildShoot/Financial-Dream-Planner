import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, r2_score


# Load dataset
df = pd.read_csv("data/salary_data.csv")


# Remove unnecessary empty column
df = df.drop(columns=["Unnamed: 5"], errors="ignore")


print("Dataset Preview:")
print(df.head())


# Features and target

X = df[[
    "Age",
    "City",
    "Education",
    "Job_Role"
]]

y = df["Monthly_Salary"]


# Categorical columns
categorical_features = [
    "City",
    "Education",
    "Job_Role"
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Models
models = {

    "Linear Regression":
        LinearRegression(),

    "Decision Tree":
        DecisionTreeRegressor(
            random_state=42
        ),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
}


results = {}

best_model = None
best_score = float("-inf")
best_name = ""


for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    results[name] = {
        "MAE": mae,
        "R2": r2
    }

    print("\n----------------------")

    print(name)

    print("MAE:", round(mae, 2))

    print("R2 Score:", round(r2, 3))


    # Select best model using R2 score
    if r2 > best_score:

        best_score = r2

        best_model = pipeline

        best_name = name


print("\n======================")

print("BEST MODEL:", best_name)

print("Best R2 Score:", round(best_score, 3))


# Create models folder
os.makedirs(
    "models",
    exist_ok=True
)


# Save best model

joblib.dump(
    best_model,
    "models/salary_model.pkl"
)


print("\nModel saved successfully!")