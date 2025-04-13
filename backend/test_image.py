from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)


def test_health_endpoint():
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200, "Health check should return 200 OK"
    response_json = response.json()
    assert "status" in response_json, "Response should include 'status' field"
    assert (
        response_json["status"] == "healthy"
    ), "Health check status should be 'healthy'"

    # Print useful information
    print(f"Health status: {response_json['status']}")


def test_predict_endpoint():
    """
    Test the /predict endpoint.
    """
    # Path to test image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image_path = os.path.join(current_dir, "bulk waste.jpeg")

    # Read test image
    with open(test_image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Send request to the endpoint
    response = client.post(
        "/predict", files={"file": ("test_image.png", image_bytes, "image/png")}
    )

    # Basic assertions
    assert response.status_code == 200, "API should return 200 OK"
    response_json = response.json()
    assert "path" in response_json, "Response should include 'path' field"
    assert (
        "predicted_value" in response_json
    ), "Response should include 'predicted_value' field"
    assert (
        "predicted_accuracy" in response_json
    ), "Response should include 'predicted_accuracy' field"

    # Print useful information
    print(f"Predicted value: {response_json['predicted_value']}")
    print(f"Predicted accuracy: {response_json['predicted_accuracy']}%")


def test_predict_test_endpoint():
    """
    Test the /predict_test endpoint.
    """
    # Path to test image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_image_path = os.path.join(current_dir, "bulk waste.jpeg")

    # Read test image
    with open(test_image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Send request to the endpoint
    response = client.post(
        "/predict_test", files={"file": ("test_image.png", image_bytes, "image/png")}
    )

    # Basic assertions
    assert response.status_code == 200, "API should return 200 OK"
    response_json = response.json()
    assert "path" in response_json, "Response should include 'path' field"
    assert (
        "predicted_value" in response_json
    ), "Response should include 'predicted_value' field"
    assert (
        "predicted_accuracy" in response_json
    ), "Response should include 'predicted_accuracy' field"

    # Print useful information
    print(f"Predicted value: {response_json['predicted_value']}")
    print(f"Predicted accuracy: {response_json['predicted_accuracy']}%")
