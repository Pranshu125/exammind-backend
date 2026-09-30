from core.config import settings
from models.schemas import VideoResource

def fetch_youtube_videos(query: str, max_results: int = 3) -> list[VideoResource]:
    if settings.YOUTUBE_API_KEY and settings.YOUTUBE_API_KEY != "YOUR_YOUTUBE_API_KEY_HERE" and settings.YOUTUBE_API_KEY != "your_youtube_api_key":
        try:
            from googleapiclient.discovery import build
            youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)
            request = youtube.search().list(
                q=query + " tutorial education",
                part="snippet",
                type="video",
                maxResults=max_results,
                videoSyndicated="true"
            )
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                videos.append(VideoResource(
                    title=item["snippet"]["title"],
                    video_id=item["id"]["videoId"],
                    thumbnail_url=item["snippet"]["thumbnails"]["high"]["url"],
                    channel_title=item["snippet"]["channelTitle"]
                ))
            return videos
        except Exception as e:
            print(f"Error fetching YouTube videos via API: {e}")
            pass # Fall back to duckduckgo

    # Fallback to DuckDuckGo Search
    print("Using DuckDuckGo Search fallback for videos.")
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.videos(
                keywords=query + " tutorial",
                max_results=max_results,
            ))
            
            videos = []
            for r in results:
                url = r.get('content', '')
                vid_id = ""
                if "v=" in url:
                    vid_id = url.split("v=")[-1].split("&")[0]
                elif "youtu.be/" in url:
                    vid_id = url.split("youtu.be/")[-1].split("?")[0]
                    
                videos.append(VideoResource(
                    title=r.get("title", f"{query} Video"),
                    video_id=vid_id if vid_id else url,
                    thumbnail_url=r.get("images", {}).get("large", f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg" if vid_id else ""),
                    channel_title=r.get("publisher", "YouTube")
                ))
            if not videos:
                raise ValueError("No videos returned from DDGS")
            return videos
    except Exception as e:
        print(f"Error fetching videos via DDGS: {e}")
        # Extreme fallback to ensure we don't return an empty array that breaks UI expectation
        # Give a generic youtube search link
        return [
            VideoResource(
                title=f"Search YouTube for {query}",
                video_id=f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                thumbnail_url="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=500&h=300&fit=crop",
                channel_title="YouTube Search"
            )
        ]
