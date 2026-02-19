# YouTube Channel Downloader

Bulk-download every video from a YouTube channel or playlist as MP4. Skips already-downloaded videos on re-run.

## Configuration

Edit `config.yaml` before running:

```yaml
YOUTUBE_CONFIG:
    API_KEY: "your_youtube_api_key"
    CHANNEL_ID: "@ChannelHandle"
    PLAYLIST_ID: ""
```

| Field | Description |
|---|---|
| `API_KEY` | Your [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) key |
| `CHANNEL_ID` | Channel handle (e.g. `@ViceGripGarage`) or channel ID |
| `PLAYLIST_ID` | Optional — leave empty to download all uploads, or set a specific playlist ID. The ID is the `list` parameter from the playlist URL, e.g. `https://www.youtube.com/playlist?list=PLEB90X8dyC-AgB_sFAvPtn1ILI-f4kCWx` → `PLEB90X8dyC-AgB_sFAvPtn1ILI-f4kCWx` |

## Installation

Requires Python 3.10+ and [FFmpeg](https://ffmpeg.org/download.html).

```bash
pip install -r requirements.txt
```

## Usage

1. Fetch the video list:

```bash
python video_list.py
```

2. Download all videos:

```bash
python download.py
```

Videos are saved to `downloads/<channel_name>/` as MP4 files (max 720p, H.264).

## Windows Executable

A standalone `.exe` is automatically built on every push via GitHub Actions. Go to the **Actions** tab in the repo, open the latest **Build Windows EXE** run, and download the `windows-executable` artifact. Place `config.yaml` in the same folder as the `.exe` and run it — no Python installation needed.
