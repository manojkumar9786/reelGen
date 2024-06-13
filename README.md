# ReelGen

ReelGen is a web application that allows users to generate short reel videos from a given YouTube video. Users can specify the duration of the reels (15 seconds, 30 seconds, or 45 seconds) and the number of reels they want. The generated reels are downloadable and ready for deployment to YouTube.

## Technology Stack

- **Frontend:** React, Tailwind CSS
- **Backend:** Python (Flask)
- **Database:** MongoDB (MongoDB Atlas)
- **Hosting:** Vercel

## Features

1. **Input Fields:**
   - A form where the user can input:
     - YouTube video URL
     - Desired duration of the reels (15s, 30s, or 45s)
     - Number of reels to generate

2. **Backend Processing:**
   - Download the YouTube video.
   - Split the video into the specified number of reels of the desired duration.
   - Save the reels to a temporary storage location.

3. **Database Storage:**
   - Store the details of the reels generated (e.g., reel ID, original video URL, reel durations, etc.) in MongoDB.

4. **Reel Retrieval:**
   - Provide a way for users to download the generated reels.

## Setup and Installation

### Prerequisites

- Node.js and npm
- Python and pip
- MongoDB Atlas account (or local MongoDB instance)

### Backend Setup

1. Clone the repository:

   git clone https://github.com/manojkumar9786/reelGen
   cd reelgen

2. Set up a virtual environment and install dependencies:

    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. Run the Flask server:

   python app.py
   
Frontend Setup:

1. Navigate to the frontend directory:
   
    cd reelgen-frontend

2. Install dependencies:

   npm install

3. Run the React development server:

   npm start

Usage
1. Open your browser and go to the deployed Vercel URL.
2. Enter the YouTube video URL, desired reel duration, and number of reels.
3. Click "Generate Reels" and wait for the reels to be processed.
4. Download the generated reels from the provided links.
   
