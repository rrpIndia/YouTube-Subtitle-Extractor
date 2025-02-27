from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_subtitles(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('hi','en'), preserve_formatting=True)
        
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    
    except Exception as e:
        print("Error:", e)

print(get_yt_subtitles('udOoKORXlbY'))
      
