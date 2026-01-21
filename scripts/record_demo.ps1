# Record demo screen for 30 seconds using ffmpeg (Windows)
# Requires ffmpeg installed and in PATH
# Modify -t to change duration

$duration = 30
$out = "demo_recording.mp4"
Write-Host "Recording screen for $duration seconds to $out"

# This uses gdigrab which captures the primary display. Adjust -framerate if needed.
ffmpeg -y -f gdigrab -framerate 15 -i desktop -t 00:00:$duration -vcodec libx264 $out

Write-Host "Recording finished: $out"

# Tip: run demo_run.ps1 before or while recording to capture the steps.