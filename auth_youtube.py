"""Run this script ONCE locally to authenticate with YouTube.
It opens a browser, you approve access, then prints your token JSON.
Copy that JSON and set it as YOUTUBE_TOKEN_JSON env var on Railway."""

from google_auth_oauthlib.flow import InstalledAppFlow
import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    flow = InstalledAppFlow.from_client_config(config.YOUTUBE_CLIENT_SECRET, SCOPES)
    credentials = flow.run_local_server(port=0)
    token_json = credentials.to_json()
    print("\n✅ Authentication successful!")
    print("\nCopy everything below and set it as YOUTUBE_TOKEN_JSON on Railway:\n")
    print(token_json)


if __name__ == "__main__":
    main()
