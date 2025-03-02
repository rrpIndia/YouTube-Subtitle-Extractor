YouTube Subtitle Extractor

This Python project extracts subtitles from YouTube videos and sends the extracted information to a Telegram bot.
Features:

    Extracts subtitles from YouTube videos (supports multiple languages like Hindi and English).
    Downloads video metadata from a YouTube channel.
    Sends the extracted subtitles and video metadata to a Telegram bot.
    Handles YouTube playlists and individual video URLs.
    Uses yt-dlp for video extraction and youtube_transcript_api for subtitle extraction.

Requirements:

    Python 3.x
    Required libraries:
        yt-dlp for downloading video metadata.
        requests for sending HTTP requests to the Telegram bot.
        youtube_transcript_api for fetching subtitles.
        python-dotenv for environment variable management.

Install the required dependencies:

pip install yt-dlp requests youtube-transcript-api python-dotenv

Setup:

    Clone this repository:

git clone https://github.com/yourusername/YouTube-Subtitle-Extractor.git
cd YouTube-Subtitle-Extractor

Create a .env file in the project directory and add the following variables:

    BOT_TOKEN=your_telegram_bot_token
    CHAT_ID=your_telegram_chat_id

    Replace your_telegram_bot_token with the token for your Telegram bot (obtained from BotFather), and your_telegram_chat_id with the chat ID where you want the messages to be sent.

    Add the YouTube channel URLs to a text file (e.g., channels.txt), one URL per line.

Running the Script:

To run the script and extract subtitles from YouTube videos, simply run:

python main.py

This will:

    Fetch video URLs from the specified channels.
    Download video metadata and extract subtitles.
    Send the subtitle and metadata to the specified Telegram chat.
