import requests
# quick test to see if restmethod is working w/ python
url = "http://127.0.0.1:8000/predict"
payload = {"text": "Testing my HuggingFace API!"} #any JSON
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
