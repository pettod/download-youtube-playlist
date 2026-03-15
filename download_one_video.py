#!/usr/bin/env python3
"""Download a single YouTube video in full HD (1080p)."""

from __future__ import annotations

import argparse
import os
import sys

import yt_dlp


def download_video_full_hd(
    url: str,
    output_dir: str = ".",
    output_template: str = "%(title)s [%(id)s].%(ext)s",
) -> str | None:
    """
    Download a YouTube video in full HD (1080p).

    Args:
        url: YouTube video URL.
        output_dir: Directory to save the file (default: current directory).
        output_template: yt-dlp output template (default: title and id).

    Returns:
        Path to the downloaded file, or None if download failed.
    """
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, output_template)

    # Prefer 1080p; merge video+audio; fallback to best available up to 1080p
    ydl_opts = {
        "format": (
            "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[acodec^=mp4a]/"
            "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/"
            "best[height<=1080][ext=mp4]/best[height<=1080]/best"
        ),
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
        "postprocessor_args": {
            "FFmpegVideoConvertor": [
                "-c:v", "libx264",
                "-c:a", "aac",
                "-movflags", "+faststart",
            ],
        },
        "retries": 3,
        "fragment_retries": 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                return None
            return ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {e}", file=sys.stderr)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a YouTube video in full HD (1080p).",
        epilog="Put the URL in quotes. Example: python download_one_video.py 'https://www.youtube.com/watch?v=VIDEO_ID'",
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        help="YouTube video URL (e.g. https://www.youtube.com/watch?v=VIDEO_ID)",
    )
    args = parser.parse_args()

    if not args.url or not args.url.strip():
        parser.print_help()
        print("\nError: Please provide a YouTube video URL.", file=sys.stderr)
        print("Add the URL inside quotes: python download_one_video.py 'https://www.youtube.com/watch?v=VIDEO_ID'", file=sys.stderr)
        sys.exit(1)

    path = download_video_full_hd(args.url.strip())
    if path is None:
        sys.exit(1)
    print(f"Downloaded: {path}")


if __name__ == "__main__":
    main()
