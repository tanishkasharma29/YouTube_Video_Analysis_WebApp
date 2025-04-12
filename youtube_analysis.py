# youtube_analysis.py

from googleapiclient.discovery import build
import pandas as pd

def get_youtube_service(api_key):
    return build("youtube", "v3", developerKey=api_key)

def get_video_details(video_id, api_key):
    youtube = get_youtube_service(api_key)
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()

    if not response["items"]:
        return None

    video = response["items"][0]
    snippet = video["snippet"]
    stats = video["statistics"]

    return {
        "Video ID": video_id,
        "Title": snippet.get("title"),
        "Published At": snippet.get("publishedAt"),
        "Channel Title": snippet.get("channelTitle"),
        "Views": int(stats.get("viewCount", 0)),
        "Likes": int(stats.get("likeCount", 0)),
        "Comments": int(stats.get("commentCount", 0)),
    }

def get_channel_stats(channel_id, api_key):
    youtube = get_youtube_service(api_key)
    request = youtube.channels().list(part="snippet,statistics", id=channel_id)
    response = request.execute()

    if not response["items"]:
        return None

    channel = response["items"][0]
    snippet = channel["snippet"]
    stats = channel["statistics"]

    return {
        "Channel Title": snippet.get("title"),
        "Subscribers": int(stats.get("subscriberCount", 0)),
        "Total Views": int(stats.get("viewCount", 0)),
        "Total Videos": int(stats.get("videoCount", 0)),
        "Description": snippet.get("description"),
    }

def get_video_comments(video_id, api_key, max_results=10):
    youtube = get_youtube_service(api_key)
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        top_comment = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "Author": top_comment["authorDisplayName"],
            "Comment": top_comment["textDisplay"],
            "Likes": top_comment["likeCount"],
            "Published": top_comment["publishedAt"]
        })

    return pd.DataFrame(comments)
