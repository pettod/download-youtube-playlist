import json
import yaml
from pydantic import BaseModel
from typing import List
from googleapiclient.discovery import build

with open('config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)
YOUTUBE_CHANNEL_ID = CONFIG["YOUTUBE_CONFIG"]["CHANNEL_ID"]
YOUTUBE_PLAYLIST_ID = CONFIG["YOUTUBE_CONFIG"]["PLAYLIST_ID"]
YOUTUBE_API_KEY = CONFIG["YOUTUBE_CONFIG"]["API_KEY"]

CACHE_FILE = f"{YOUTUBE_CHANNEL_ID.replace('@', '').lower()}.json"
YOUTUBE_API = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Data schema
class YouTubeVideo(BaseModel):
    id: str
    url: str
    title: str
    date: str


def get_all_video_urls(channel_id: str) -> List[YouTubeVideo]:
    # Get the "Uploads" Playlist ID for the channel
    if channel_id.startswith("@"):
        ch_request = YOUTUBE_API.channels().list(part="contentDetails", forHandle=channel_id)
    else:
        ch_request = YOUTUBE_API.channels().list(part="contentDetails", id=channel_id)
    ch_response = ch_request.execute()

    if not ch_response.get('items'):
        raise ValueError(f"No channel found for: {channel_id}")
    
    if YOUTUBE_PLAYLIST_ID != "":
        uploads_playlist_id = YOUTUBE_PLAYLIST_ID
    else:
        uploads_playlist_id = ch_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Fetch videos from that playlist
    videos = []
    next_page_token = None
    
    while True:
        pl_request = YOUTUBE_API.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        
        for item in pl_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_data = YouTubeVideo(
                id=video_id,
                url=f"https://www.youtube.com/watch?v={video_id}",
                title=item['snippet']['title'],
                date=item['snippet']['publishedAt'],
            )
            videos.append(video_data)
        
        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break

    save_videos(videos)
    return videos


def save_videos(videos: List[YouTubeVideo]):
    with open(CACHE_FILE, "w") as f:
        json.dump([v.model_dump() for v in videos], f, indent=4)


def main():
    all_videos = get_all_video_urls(YOUTUBE_CHANNEL_ID) 
    print(f"Found {len(all_videos)} videos")
    for v in all_videos[:10]:
        print(f"{v.date} - {v.title}: {v.url}")


if __name__ == "__main__":
    main()
