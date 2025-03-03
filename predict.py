import requests

# Define the FastAPI endpoint
url = "http://localhost:8000/predict"

# Example input (single row of features)
sample_input = {
    "features": [
        1.2,
        -0.3,
        0.0,
        -0.1,
        0.8,
        0.7,
        -1.2,
        0.3,
        1.5,
        -0.8,
        0.9,
        -0.5,
        0.2,
        1.3,
        -0.4,
        0.6,
        -1.0,
        0.7,
        -0.6,
        0.8,
    ]
}

# Send request to FastAPI
response = requests.post(url, json=sample_input)

# Print response
print(response.json())
