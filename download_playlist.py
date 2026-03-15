import json
import os
import yt_dlp
import yaml
from tqdm import tqdm
from video_list import get_all_video_urls


with open('config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)
YOUTUBE_CHANNEL_ID = CONFIG["YOUTUBE_CONFIG"]["CHANNEL_ID"]
YOUTUBE_PLAYLIST_ID = CONFIG["YOUTUBE_CONFIG"]["PLAYLIST_ID"]
CACHE_FILE = f"{YOUTUBE_CHANNEL_ID.replace('@', '').lower()}.json"
DOWNLOAD_DIR = f"downloads/{YOUTUBE_CHANNEL_ID.replace('@', '').lower()}"


def load_videos(cache_file):
    if not os.path.exists(cache_file):
        return []
    with open(cache_file, "r") as f:
        return json.load(f)


def download_videos(videos, download_dir):
    os.makedirs(download_dir, exist_ok=True)

    already_downloaded = set()
    for filename in os.listdir(download_dir):
        video_id = filename.rsplit(".", 1)[0].rsplit(" [", 1)[-1].rstrip("]")
        already_downloaded.add(video_id)

    ydl_opts = {
        "format": "bestvideo[height<=720][vcodec^=avc1]+bestaudio[acodec^=mp4a]/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]/best",
        "outtmpl": os.path.join(download_dir, "%(title)s [%(id)s].%(ext)s"),
        "merge_output_format": "mp4",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
        "postprocessor_args": {
            "FFmpegVideoConvertor": ["-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart"],
        },
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": False,
        "retries": 3,
        "fragment_retries": 3,
    }

    total = len(videos)
    skipped = 0
    downloaded = 0
    failed = 0
    failed_videos = []

    for video in tqdm(videos):
        video_id = video["id"]
        title = video["title"]
        url = video["url"]

        if video_id in already_downloaded:
            skipped += 1
            continue

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            downloaded += 1
        except Exception as e:
            failed_videos.append(title)
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done! Total: {total}")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped:    {skipped}")
    print(f"  Failed:     {failed}")
    print(f"  Failed videos: {failed_videos}")


if __name__ == "__main__":
    videos = load_videos(CACHE_FILE)
    if not videos:
        videos = get_all_video_urls(YOUTUBE_CHANNEL_ID)
        videos = load_videos(CACHE_FILE)
    print(f"Found {len(videos)} videos in {CACHE_FILE}")
    download_videos(videos, DOWNLOAD_DIR)
