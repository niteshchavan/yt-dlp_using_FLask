import os
import time
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def download_video(video_url, download_dir):
    import yt_dlp

    ydl_opts_720p = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': '22',  # Format 22 represents 720p resolution
    }

    ydl_opts_360p = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': '18',  # Format 18 represents 360p resolution
    }

    # First, try to download in 720p resolution (format 22)
    with yt_dlp.YoutubeDL(ydl_opts_720p) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'Unknown')
            return video_title
        except yt_dlp.DownloadError:
            # If 720p format is not available, fallback to 360p resolution (format 18)
            with yt_dlp.YoutubeDL(ydl_opts_360p) as ydl:
                try:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_title = info_dict.get('title', 'Unknown')
                    return video_title
                except yt_dlp.DownloadError as e:
                    print(f"Error: {str(e)}")
                    return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def initiate_download():
    video_url = request.form['video_url']
    if not video_url:
        return "Error: Please provide a video URL"

    # Provide the path where you want to save the downloaded videos
    download_dir = os.path.join(os.getcwd(), 'downloads')

    # Call the download function and get the video title
    video_title = download_video(video_url, download_dir)

    if video_title:
        return jsonify({'video_title': video_title})
    else:
        return "Error: Download failed"

if __name__ == '__main__':
    app.run(debug=True)
