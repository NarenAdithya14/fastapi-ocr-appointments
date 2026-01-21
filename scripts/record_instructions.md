Recording instructions (short)

Option A — OBS Studio (recommended):
1. Install OBS Studio (https://obsproject.com/).
2. Create a new Scene and add a "Window Capture" or "Display Capture".
3. Start your server:
   .\.venv\Scripts\python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
4. Open http://127.0.0.1:8000/docs
5. In OBS press Start Recording, run the examples in the Swagger UI or run curl commands, stop recording, and save.

Option B — ffmpeg (command-line recording):
# Example: record primary monitor for 20 seconds (Windows)
ffmpeg -f gdigrab -framerate 15 -i desktop -t 00:00:20 -vcodec libx264 demo.mp4

Tips:
- Keep the recording short (30-60s) showing the /docs call and one curl.
- Upload the resulting mp4 to your GitHub release, Google Drive, or include it in the submission ZIP.
