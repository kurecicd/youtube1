import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _get_youtube_client():
    creds = Credentials.from_authorized_user_info(
        json.loads(config.YOUTUBE_TOKEN), scopes=SCOPES
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def upload_video(video_path: str, script: dict) -> str:
    youtube = _get_youtube_client()

    body = {
        "snippet": {
            "title": script["title"],
            "description": script["description"],
            "tags": script["tags"],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": True,
            "selfDeclaredMadeForKids": True,
        },
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        _, response = request.next_chunk()

    video_id = response["id"]
    print(f"  Uploaded: https://youtube.com/shorts/{video_id}")
    return video_id
