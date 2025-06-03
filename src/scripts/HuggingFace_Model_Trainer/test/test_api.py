# test_api.py
import requests

def test_positive_sentiment():
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"text": "Testing my HuggingFace API!"},
        headers={"Content-Type": "application/json"}
    )
    result = response.json()
    assert result["label"] == "POSITIVE"
    assert result["score"] > 0.8
