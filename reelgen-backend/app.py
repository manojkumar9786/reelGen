from flask import Flask, request, send_file, jsonify
from flask_pymongo import PyMongo
from moviepy.editor import VideoFileClip
from flask_cors import CORS
from pytube import YouTube
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure MongoDB connection
app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
mongo = PyMongo(app)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/api/generate-reels', methods=['POST'])
def generate_reels():
    data = request.json
    video_url = data['url']
    duration = data['duration']
    number_of_reels = data['numberOfReels']

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4').first()
        video_path = stream.download(output_path=DOWNLOAD_FOLDER)
        
        print(f"Video downloaded to: {video_path}")

        clip = VideoFileClip(video_path)
        video_filename = secure_filename(yt.title)
        reel_filenames = []

        for i in range(number_of_reels):
            start_time = i * duration
            end_time = start_time + duration
            reel_filename = f"{video_filename}_reel_{i + 1}.mp4"
            reel_path = os.path.join(DOWNLOAD_FOLDER, reel_filename)

            # Create subclip
            reel_clip = clip.subclip(start_time, min(end_time, clip.duration))
            reel_clip.write_videofile(reel_path, codec="libx264")

            # Debugging: Check created reel path
            print(f"Reel {i + 1} created at: {reel_path}")

            # Store reel filename
            reel_filenames.append(reel_filename)

        # Save reel details to MongoDB
        reel_data = {
            'original_video_url': video_url,
            'reel_filenames': reel_filenames,
            'duration': duration,
            'number_of_reels': number_of_reels
        }
        mongo.db.reels.insert_one(reel_data)

        return jsonify({'message': 'Reels generated successfully', 'reel_filenames': reel_filenames}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reels', methods=['GET'])
def get_reels():
    reels = mongo.db.reels.find()
    result = []
    for reel in reels:
        reel['_id'] = str(reel['_id'])
        result.append(reel)
    return jsonify(result)

@app.route('/api/download-reel/<filename>', methods=['GET'])
def download_reel(filename):
    try:
        # Debugging: Check filename received
        print(f"Download requested for: {filename}")
        return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
