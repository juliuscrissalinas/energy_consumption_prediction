# filepath: /Users/juliuscrissalinas/Documents/MSDS/ML_Ops/docker/docker_exer/mlflow_demo.py
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from loguru import logger

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

import shap
import matplotlib.pyplot as plt
from typing import Dict


# Generate synthetic data
def generate_synthetic_data():
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
    return df, y


df, y = generate_synthetic_data()
X = df.values  # Convert DataFrame to numpy array

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define hyperparameter grid for tuning
param_grid: Dict[str, list] = {
    "n_estimators": [50, 100],
    "learning_rate": [0.01, 0.1],
    "max_depth": [3, 5],
    "subsample": [0.8, 1.0],
}

# Perform hyperparameter tuning using GridSearchCV
gb = GradientBoostingClassifier()
grid_search = GridSearchCV(gb, param_grid, cv=3, scoring="accuracy", n_jobs=-1)
grid_search.fit(X_train, y_train)

# Retrieve the best model from the grid search
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

# Calculate metrics
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "f1_score": f1_score(y_test, y_pred),
    "roc_auc": roc_auc_score(y_test, y_proba),
}

mlflow.set_tracking_uri("http://localhost:5000")
with mlflow.start_run():
    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metrics(metrics)
    mlflow.set_tag("model_description", "Gradient Boosting Classifier trained with GridSearchCV for hyperparameter tuning.")

    # Log the trained model with inferred input signature
    signature = infer_signature(X_train, best_model.predict(X_train))
    model_info = mlflow.sklearn.log_model(best_model, "gradient_boosting_model", signature=signature)

    # SHAP feature importance analysis
    explainer = shap.Explainer(best_model, X_train)
    shap_values = explainer(X_test[:100])

    # Generate and log SHAP summary plot
    shap_plot_path = "shap_summary_plot.png"
    plt.figure()
    shap.summary_plot(shap_values, X_test[:100], show=False)
    plt.savefig(shap_plot_path, bbox_inches="tight")
    plt.close()
    mlflow.log_artifact(shap_plot_path)

    # **Register the model in the MLflow Model Registry**
    model_uri = model_info.model_uri  # Get the logged model's URI
    registered_model = mlflow.register_model(model_uri, "GradientBoostingClassifier")


logger.info("Best Parameters: {}", grid_search.best_params_)
logger.info("Evaluation Metrics: {}", metrics)