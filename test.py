import mlflow.sklearn

# Set MLflow tracking server (ensure this matches your MLflow server address)
mlflow.set_tracking_uri("http://localhost:5000")

# Load the registered model
model_uri = "models:/gradient_boosting_model/1"  # Use "latest" if you always want the newest version
model = mlflow.sklearn.load_model(model_uri)

print("Model loaded successfully!")