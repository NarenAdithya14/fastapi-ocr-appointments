# Demo runner (PowerShell)
# Starts the FastAPI server, runs two sample curl requests (success + ambiguous), and saves responses.
# Requires: .venv present and activated or use the full path to venv python.

$python = ".\.venv\Scripts\python.exe"
$uvicornArgs = "-m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000"

Write-Host "Starting uvicorn in background..."
Start-Process -FilePath $python -ArgumentList $uvicornArgs
Start-Sleep -Seconds 2

# Run a success example
$success = curl -s -X POST http://127.0.0.1:8000/appointments -H "Content-Type: application/json" -d '{"text":"Schedule a meeting with John Doe on March 10th at 3 PM."}'
$success | Out-File -FilePath demo_success.json -Encoding utf8
Write-Host "Saved demo_success.json"

# Run an ambiguous example
$amb = curl -s -X POST http://127.0.0.1:8000/appointments -H "Content-Type: application/json" -d '{"text":"Let's meet next week."}'
$amb | Out-File -FilePath demo_ambiguous.json -Encoding utf8
Write-Host "Saved demo_ambiguous.json"

Write-Host "Demo requests complete. Stop the uvicorn process manually when done."