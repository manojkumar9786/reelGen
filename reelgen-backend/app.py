from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import uuid
import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

client = MongoClient('mongodb://localhost:27017/reelgen')
db = client.reelgen

# Directory to store generated reels
REELS_DIRECTORY = 'reels_storage'
if not os.path.exists(REELS_DIRECTORY):
    os.makedirs(REELS_DIRECTORY)

@app.route('/api/generate-reels', methods=['POST'])
def generate_reels():
    try:
        data = request.json
        url = data['url']
        duration = data['duration']
        number_of_reels = data['numberOfReels']

        # Download the YouTube video
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download(filename='video.mp4')
        logging.info(f'Video downloaded to {video_path}')

        # Split the video
        video = VideoFileClip(video_path)
        reels = []
        for i in range(number_of_reels):
            start_time = i * duration
            end_time = start_time + duration
            if end_time > video.duration:
                break
            reel_filename = f'reel_{uuid.uuid4()}.mp4'
            reel_path = os.path.join(REELS_DIRECTORY, reel_filename)
            video.subclip(start_time, end_time).write_videofile(reel_path)
            reels.append(reel_filename)
            # Store details in MongoDB
            db.reels.insert_one({
                'reel_id': str(uuid.uuid4()),
                'original_url': url,
                'reel_filename': reel_filename,
                'duration': duration,
                'created_at': datetime.datetime.now()
            })
            logging.info(f'Reel generated and stored at {reel_path}')

        video.close()
        os.remove(video_path)
        logging.info(f'Original video file {video_path} removed')

        return jsonify({'reels': reels})

    except Exception as e:
        logging.error(f'Error occurred: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-reel/<filename>', methods=['GET'])
def download_reel(filename):
    try:
        return send_from_directory(REELS_DIRECTORY, filename, as_attachment=True)
    except Exception as e:
        logging.error(f'Error occurred while sending file: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(db.reels.find({}, {'_id': 0}))
        return jsonify(reels)
    except Exception as e:
        logging.error(f'Error occurred while fetching reels: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
