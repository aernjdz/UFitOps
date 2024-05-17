from flask import Flask, send_from_directory, render_template,request,jsonify
from flask_bootstrap import Bootstrap5
import os
import yt_dlp

app = Flask(__name__)
bootstrap = Bootstrap5(app)

trending_url = 'https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D'
@app.route('/')
@app.route('/index')
def hello_world():
    return render_template("main.html", song=get_trending_song(trending_url), songs = get_trending_songs(trending_url))

@app.route("/SeAll_Songs")
def seAll_songs():
    return render_template("seeAll.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))
def format_duration(seconds):
    if seconds is None:
        return "Unknown Duration"
    minutes, seconds = divmod(seconds, 60)
    if seconds < 10 and minutes < 10:
        return f"{'0'+str(int(minutes))}:{'0'+str(int(seconds))}"
    elif seconds < 10:
        return f"{int(minutes)}:{'0'+str(int(seconds))}"
    elif minutes < 10:
        return f"{'0'+str(int(minutes))}:{int(seconds)}"
    else:
        return f"{int(minutes)}:{int(seconds)}"
    
@app.route('/get_audio_stream_url', methods=['GET'])
def get_audio_stream_url():
    song_url = request.args.get('song_url')
    ydl_opts = {
        'quiet': True,      # Suppress console output
        'format': 'bestaudio/best',  # Choose the best audio format available
         'youtube_include_dash_manifest': False,  # Disable DASH manifest fetching
    'ignoreerrors': True,          # Ignore download errors
        'geturl': True,     # Only get the direct URL
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(song_url , download=False)
        if 'url' in info_dict:
         
            return jsonify({'audio_stream_url': info_dict['url']})
        else:
            return None

# Example usage


def get_trending_song(url:str)->list:
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': 1,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        
            video = info.get('entries', [])
        

           
            songs = {
                    'title': video[0]['title'],
                    'thumbnails': video[0]['thumbnails'][0]['url'],
                    'url': f"https://www.youtube.com/watch?v={video[0]['id']}",
                    'artist': video[0].get('uploader', 'Unknown Artist'),
                    'views': video[0].get('view_count', 'Unknown Views'),
             
                }
              
            
          
            return songs

        except Exception as e:
            print(f"An error occurred: {e}")
            return []


def get_trending_songs(url : str)->list:
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': 4,
        'quiet': True
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
           
            videos = info.get('entries', [])
           
            for video in videos:
                print(f"Title: {video['title']}, ID: {video['id']}, Uploader: {video.get('uploader')}, Views: {video.get('view_count')}")
               
            songs = [
                {
                    "id" : i+1,
                    'title': videos[i]['title'],
                    'url': f"https://www.youtube.com/watch?v={videos[i]['id']}",
                    'thumbnails': videos[i]['thumbnails'][0]['url'],
                    'artist': videos[i].get('uploader', 'Unknown Artist'),
                    'views': f"{videos[i].get('view_count', 'Unknown Views')} Plays",
                    'duration': format_duration(videos[i].get('duration', 'Unknown Duration')),
                    
                }
                for i in range(4) 
            ]
            return songs

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

def get_trending_songs_to20(url : str)->list:
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': 30,
        'quiet': True
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
           
            videos = info.get('entries', [])
           
            for video in videos:
                print(f"Title: {video['title']}, ID: {video['id']}, Uploader: {video.get('uploader')}, Views: {video.get('view_count')}")
               
            songs = [
                {
                    "id" : i+1,
                    'title': videos[i]['title'],
                    'url': f"https://www.youtube.com/watch?v={videos[i]['id']}",
                    'thumbnails': videos[i]['thumbnails'][0]['url'],
                    'artist': videos[i].get('uploader', 'Unknown Artist'),
                    'views': f"{videos[i].get('view_count', 'Unknown Views')} Plays",
                    'duration': format_duration(videos[i].get('duration', 'Unknown Duration')),
                    
                }
                for i in range(30) 
            ]
            return songs

        except Exception as e:
            print(f"An error occurred: {e}")
            return []


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.208", port=1939)
