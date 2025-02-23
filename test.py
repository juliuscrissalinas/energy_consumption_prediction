import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    mlflow.log_param("param1", 42)
    mlflow.log_metric("accuracy", 0.95)

print("Test run logged successfully!")
