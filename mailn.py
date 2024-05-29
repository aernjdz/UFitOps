from flask import Flask, send_from_directory, render_template,request,jsonify, redirect, url_for,Response
from flask_bootstrap import Bootstrap5
import os
import yt_dlp
import json
import yt_dlp
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
bootstrap = Bootstrap5(app)
#q
trending_url = 'https://music.youtube.com/playlist?list=PL4fGSI1pDJn7524WZdmWAIRc6cQ3vUzZK'
@app.route('/')
@app.route('/index')
def hello_world():
    username = "Login"
    return render_template("main.html", song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url),user=(username))


@app.route('/genres')
def genres():
    return render_template("genres.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))

@app.route('/albums')
def albums():
    return render_template("albums.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))

@app.route('/artists')
def artists():
    return render_template("artists.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))

@app.route('/podcasts')
def podcasts():
    return render_template("podcasts.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))

@app.route("/SeAll_Songs")
def seAll_songs():
    return render_template("seeAll.html",song=get_trending_song(trending_url), songs = get_trending_songs_to20(trending_url))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # /login?username=name?password=pass q
        username = request.form['username']
        password = request.form['password']
        print(username,password)

        if username !="" and password!="":
            if username=="":
                username="Login"
            return render_template("main.html", song=get_trending_song(trending_url), songs = get_trending_songs(trending_url), user = (username))
        else:
            ...
    return render_template('login.html')


@app.route('/proxy_audio', methods=['GET'])
def proxy_audio():
    audio_url = request.args.get('audio_url')
    if not audio_url:
        return jsonify({"error": "Missing audio_url parameter"}), 400

    try:
        # Fetch the audio content
        response = requests.get(audio_url, stream=True)
        response.raise_for_status()

        # Stream the audio content back to the client with appropriate headers
        return Response(
            response.iter_content(chunk_size=10 * 1024),
            content_type=response.headers['Content-Type'],
            headers={
                'Access-Control-Allow-Origin': '*',
                'Content-Disposition': 'inline; filename="audio.webm"',
                'Content-Length': response.headers['Content-Length']
            }
        )
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/signin', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullName']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirmPass = request.form['confirmPass']
        
        if username!="" and email!="" and password!="":
            return redirect('login.html')
        else:
           # flash("Please fill in all fields", "error")
            Er = "Invalid username or password."
            return redirect(('signin.html'),error=(Er))
    return render_template('signin.html')


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

@app.route('/get_song_info', methods=['GET'])
def get_song_info():
    url = request.args.get('song_url')
    
    if not url:
        return jsonify({'error': 'Missing song_url parameter'}), 400
    
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': 1,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                video = info['entries'][0]
            else:
                video = info
            
            title = video.get('title', 'Unknown Title')
            thumbnails = video.get('thumbnails', [{}])[0].get('url', '')
            video_url = f"https://music.youtube.com/watch?v={video.get('id', '')}"
            artist = video.get('uploader', 'Unknown Artist')
            views = video.get('view_count', 'Unknown Views')
            
            return jsonify({
                'title': title,
                'thumbnails': thumbnails,
                'url': video_url,
                'artist': artist,
                'views': views
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


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
                    'url': f"https://music.youtube.com/watch?v={video[0]['id']}",
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
        'playlistend': 5,
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
                    "title": videos[i]['title'],
                    "url": f"https://music.youtube.com/watch?v={videos[i]['id']}",
                    "thumbnails": videos[i]['thumbnails'][0]['url'],
                    "artist": videos[i].get('uploader', 'Unknown Artist'),
                    "views": f"{videos[i].get('view_count', 'Unknown Views')} Plays",
                    "duration": format_duration(videos[i].get('duration', 'Unknown Duration')),
                    
                }
                for i in range(5) 
            ]
            print(songs)
            return songs

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

def get_trending_songs_to20(url : str)->list:
    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': 100,
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
                    'url': f"https://music.youtube.com/watch?v={videos[i]['id']}",
                    'thumbnails': videos[i]['thumbnails'][0]['url'],
                    'artist': videos[i].get('uploader', 'Unknown Artist'),
                    'views': f"{videos[i].get('view_count', 'Unknown Views')} Plays",
                    'duration': format_duration(videos[i].get('duration', 'Unknown Duration')),
                    
                }
                for i in range(100) 
            ]
            return songs

        except Exception as e:
            print(f"An error occurred: {e}")
            return []















































def search_song_by_title(title: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extract_flat': 'in_playlist',
        'default_search': 'ytsearch1',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_results = ydl.extract_info(title, download=False)
            video = search_results['entries'][0]

            song_info = {
                'title': video['title'],
                'thumbnails': video['thumbnails'][0]['url'],
                'url': f"https://www.youtube.com/watch?v={video['id']}",
                'artist': video.get('uploader', 'Unknown Artist'),
                'views': video.get('view_count', 'Unknown Views'),
                'audio_stream_url': video['url']
            }

            return song_info

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

@app.route('/search_song', methods=['GET'])
def search_song():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    song_info = search_song_by_title(title)
    if not song_info:
        return jsonify({'error': 'Song not found'}), 404

    return jsonify(song_info)























if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.208", port=1939)
