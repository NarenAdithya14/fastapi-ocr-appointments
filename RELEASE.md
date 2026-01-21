# Release instructions

1. Build & test locally

   ```powershell
   .\.venv\Scripts\python -m pip install --upgrade pip
   .\.venv\Scripts\python -m pip install -r requirements.txt
   .\.venv\Scripts\python -m pytest -q
   ```

2. Record demo video

   - Use `scripts\demo_run.ps1` to run the sample requests and save outputs.
   - Use `scripts\record_demo.ps1` to capture your screen for ~30s (ensure ffmpeg is installed).

3. Create GitHub repo and push

   - Create a repository named `fastapi-ocr-appointments` under user `Narenadithya14`.
   - Run `scripts\publish_to_github.ps1` (it will prompt you to authenticate if needed).

4. Create a Release and attach the recorded mp4

   - Go to GitHub > Your repo > Releases > Draft a new release.
   - Attach `demo_recording.mp4` and add release notes (what's included, how to run).

5. Share

   - Share the repo link and the release link as your submission.
