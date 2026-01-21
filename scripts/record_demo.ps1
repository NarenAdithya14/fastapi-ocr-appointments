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

# After recording you can create a GIF using ffmpeg. Example commands:
# Convert recorded MP4 to GIF (simple palette method):
# ffmpeg -y -i demo_recording.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png
# ffmpeg -y -i demo_recording.mp4 -i palette.png -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" demo.gif

# Or create a short GIF directly (trim to first 10 seconds):
# ffmpeg -y -ss 0 -t 10 -i demo_recording.mp4 -vf "fps=15,scale=480:-1:flags=lanczos" demo_short.gif