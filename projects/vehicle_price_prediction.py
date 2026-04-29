import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# STEP 1: DATA LOADING & EXPLORATION
# ==========================================
print("--- Step 1: Loading & Exploring Data ---")
df = pd.read_csv("tata_vehicle_price_dataset_v2.csv")

print(f"Dataset Shape: {df.shape}")
print("\nBasic Info:")
print(df.info())
print("\nFirst 5 Rows:")
print(df.head())

# Confirming no missing values or duplicates
print(f"\nMissing Values:\n{df.isnull().sum().sum()}")
print(f"Duplicate Rows: {df.duplicated().sum()}")

# ==========================================
# STEP 2: DATA PREPROCESSING
# ==========================================
print("\n--- Step 2: Data Preprocessing ---")

# Separate features (X) and target (y)
X = df.drop("Selling_Price", axis=1)
y = df["Selling_Price"]

# Identifying column types
categorical_cols = ["Car_Name", "Fuel_Type", "Transmission", "Seller_Type", "Location"]
numerical_cols = ["Year", "Car_Age", "Kms_Driven", "Owner", "Engine", "Power", "Efficiency", "Seats", "Present_Price"]

# Preprocessing Pipeline
# Note: StandardScaler is REMOVED for Random Forest as it is tree-based and doesn't require scaling.
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numerical_cols)  # Viva insight: Tree-based models don't need scaling
    ]
)

# ==========================================
# STEP 3: TRAIN-TEST SPLIT
# ==========================================
print("\n--- Step 3: Train-Test Split ---")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# ==========================================
# STEP 4: MODEL TRAINING (RANDOM FOREST)
# ==========================================
print("\n--- Step 4: Training Baseline Model ---")

# Building the baseline pipeline
baseline_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

baseline_model.fit(X_train, y_train)
print("Baseline Random Forest Model Trained.")

# ==========================================
# STEP 5: MODEL EVALUATION (BASELINE)
# ==========================================
print("\n--- Step 5: Evaluating Baseline Model ---")
y_pred = baseline_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Baseline MAE: {mae:.4f}")
print(f"Baseline R2 Score: {r2:.4f}")

# Cross-Validation Score (Stability Check)
cv_scores = cross_val_score(baseline_model, X, y, cv=5, scoring="r2")
print(f"Mean Cross-validation R2: {cv_scores.mean():.4f}")

# Overfitting Check
print(f"Baseline Train R2: {baseline_model.score(X_train, y_train):.4f}")
print(f"Baseline Test R2: {baseline_model.score(X_test, y_test):.4f}")

# ==========================================
# STEP 6: ACCURACY IMPROVEMENT (GRIDSEARCH)
# ==========================================
print("\n--- Step 6: Hyperparameter Tuning with GridSearchCV ---")

param_grid = {
    "regressor__n_estimators": [100, 200, 300],
    "regressor__max_depth": [10, 20, None],
    "regressor__min_samples_split": [2, 5],
    "regressor__min_samples_leaf": [1, 2]
}

grid_search = GridSearchCV(baseline_model, param_grid, cv=3, scoring="r2", n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

print(f"Best Parameters: {grid_search.best_params_}")

# ==========================================
# STEP 7: FINAL MODEL EVALUATION
# ==========================================
print("\n--- Step 7: Evaluating Final (Tuned) Model ---")
best_model = grid_search.best_estimator_
y_pred_final = best_model.predict(X_test)

mae_final = mean_absolute_error(y_test, y_pred_final)
r2_final = r2_score(y_test, y_pred_final)

print(f"Final MAE: {mae_final:.4f}")
print(f"Final R2 Score: {r2_final:.4f}")
print(f"Final Train R2: {best_model.score(X_train, y_train):.4f}")
print(f"Final Test R2: {best_model.score(X_test, y_test):.4f}")

# ==========================================
# STEP 8: FEATURE IMPORTANCE
# ==========================================
print("\n--- Step 8: Feature Importance ---")

# Extracting feature names after OneHotEncoding
feature_names = best_model.named_steps['preprocessor'].get_feature_names_out()
importances = best_model.named_steps['regressor'].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("Top 10 Important Features:")
print(importance_df.head(10))

# ==========================================
# STEP 9: SAVE MODELS
# ==========================================
print("\n--- Step 9: Saving Models ---")
joblib.dump(baseline_model, "baseline_model.pkl")
joblib.dump(best_model, "car_price_model.pkl")
print("Models saved: 'baseline_model.pkl' and 'car_price_model.pkl'")

print("\n--- Pipeline Complete ---")
