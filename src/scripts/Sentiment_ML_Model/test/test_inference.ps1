# test_inference.ps1
# quick test to see if restmethod is working w/ powershell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
    -Method Post `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body '{"text": "Testing my HuggingFace API!"}'

$response | Format-List
