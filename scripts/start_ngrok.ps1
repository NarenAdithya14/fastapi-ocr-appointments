# Start uvicorn and ngrok for local demo (PowerShell)
# Usage: run this from repository root in PowerShell

# Start uvicorn in a separate window (optional)
Start-Process -NoNewWindow -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m","uvicorn","src.main:app","--reload","--host","127.0.0.1","--port","8000"

Write-Host "Waiting 2s for server to boot..."
Start-Sleep -Seconds 2

# Start ngrok (assumes ngrok is in PATH)
ngrok http 8000
