# Sample client code that consumes APIs.
import requests
import io

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def get_root():
    response = requests.get(f"{BASE_URL}/")
    print("GET / ->", response.json())

def create_model():
    model_data = {
        "id": 1,
        "name": "TestModel",
        "version": "1.0",
        "description": "A test ML model",
        "trained": False
    }
    response = requests.post(f"{BASE_URL}/models", json=model_data)
    print("POST /models ->", response.json())

def list_models():
    response = requests.get(f"{BASE_URL}/models")
    print("GET /models ->", response.json())

def get_model():
    response = requests.get(f"{BASE_URL}/models/1")
    print("GET /models/1 ->", response.json())

def update_model():
    updated_model = {
        "id": 1,
        "name": "TestModel",
        "version": "1.0",
        "description": "A test ML model (updated)",
        "trained": True
    }
    response = requests.put(f"{BASE_URL}/models/1", json=updated_model)
    print("PUT /models/1 ->", response.json())

def delete_model():
    response = requests.delete(f"{BASE_URL}/models/1")
    print("DELETE /models/1 ->", response.json())

def get_prediction():
    # Sending a prediction request with query parameters
    params = {"task_id": 123, "input_feature": 5.5}
    response = requests.get(f"{BASE_URL}/predictions", params=params)
    print("GET /predictions ->", response.json())

def upload_training_data():
    # Create some dummy training data in memory.
    training_data = b"sample training data content"
    files = {"file": ("training_data.txt", training_data)}
    response = requests.post(f"{BASE_URL}/upload_training_data", files=files)
    print("POST /upload_training_data ->", response.json())

def upload_model_file():
    # Create a dummy model file in memory.
    model_file_content = b"dummy model binary content"
    # The tuple format is: (filename, fileobj or bytes, content_type)
    files = {"file": ("model.pkl", model_file_content, "application/octet-stream")}
    response = requests.post(f"{BASE_URL}/upload_model_file", files=files)
    print("POST /upload_model_file ->", response.json())

def create_item():
    # Create an item with pricing details.
    item_data = {
        "name": "TestItem",
        "description": "This is a test item",
        "price": 25.50,
        "tax": 3.50
    }
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    print("POST /items/ ->", response.json())

def create_user():
    # Create a user with advanced field validation.
    user_data = {
        "username": "testuser",
        "email": "test.user@example.com",
        "age": 30,
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print("POST /users/ ->", response.json())

def read_items_commons():
    # Test dependency injection endpoint for common query parameters.
    params = {"q": "searchterm", "skip": 10, "limit": 5}
    response = requests.get(f"{BASE_URL}/items/commons", params=params)
    print("GET /items/commons ->", response.json())

def async_example():
    response = requests.get(f"{BASE_URL}/async-example")
    print("GET /async-example ->", response.json())

def sync_example():
    response = requests.get(f"{BASE_URL}/sync-example")
    print("GET /sync-example ->", response.json())

def main():
    print("=== Testing FastAPI Endpoints ===")
    
    # 1. Test the root endpoint
    get_root()
    
    # 2. Create a new ML model
    create_model()
    
    # 3. List all ML models
    list_models()
    
    # 4. Get a specific ML model
    get_model()
    
    # 5. Update the ML model
    update_model()
    
    # 6. Get the updated ML model
    get_model()
    
    # 7. Delete the ML model
    delete_model()
    
    # 8. List models to confirm deletion
    list_models()
    
    # 9. Test prediction endpoint
    get_prediction()
    
    # 10. Upload training data file
    upload_training_data()
    
    # 11. Upload model file
    upload_model_file()

    # 12. Create an item with pricing details
    create_item()

    # 13. Create a user with advanced validation
    create_user()

    # 14. Test dependency injection endpoint (common query parameters)
    read_items_commons()

    # 15. Test async endpoint
    async_example()

    # 16. Test sync endpoint
    sync_example()

if __name__ == "__main__":
    main()
