import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Form = () => {
    const [url, setUrl] = useState('');
    const [duration, setDuration] = useState('15');
    const [numberOfReels, setNumberOfReels] = useState('1');
    const [reels, setReels] = useState([]);
    const [loading, setLoading] = useState(false); // Loading state

    const API_BASE_URL = 'http://localhost:5000/api'; // Replace with your Vercel backend URL


    

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); // Set loading to true
        try {
            await axios.post(`${API_BASE_URL}/generate-reels`, {
                url,
                duration: parseInt(duration),
                numberOfReels: parseInt(numberOfReels),
            });
            fetchReels(); // Fetch the updated list of reels
        } catch (error) {
            console.error('Error generating reels:', error);
        }
        setLoading(false); // Set loading to false
    };

    const fetchReels = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/reels`);
            setReels(response.data);
        } catch (error) {
            console.error('Error fetching reels:', error);
        }
    };

    useEffect(() => {
        fetchReels();
    }, []);

    return (
        <div className="animated-bg min-h-screen flex items-center justify-center">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-lg">
                <h1 className="text-2xl font-bold mb-6 text-center">ReelGen</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block mb-1 font-medium">YouTube Video URL</label>
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            required
                            disabled={loading} // Disable input while loading
                            className="w-full p-2 border border-gray-300 rounded"
                        />
                    </div>
                    <div>
                        <label className="block mb-1 font-medium">Reel Duration</label>
                        <select
                            value={duration}
                            onChange={(e) => setDuration(e.target.value)}
                            disabled={loading} // Disable input while loading
                            className="w-full p-2 border border-gray-300 rounded"
                        >
                            <option value="15">15 seconds</option>
                            <option value="30">30 seconds</option>
                            <option value="45">45 seconds</option>
                        </select>
                    </div>
                    <div>
                        <label className="block mb-1 font-medium">Number of Reels</label>
                        <input
                            type="number"
                            value={numberOfReels}
                            onChange={(e) => setNumberOfReels(e.target.value)}
                            min="1"
                            required
                            disabled={loading} // Disable input while loading
                            className="w-full p-2 border border-gray-300 rounded"
                        />
                    </div>
                    <button
                        type="submit"
                        className={`w-full py-2 rounded ${loading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'} text-white`}
                        disabled={loading} // Disable button while loading
                    >
                        {loading ? (
                            <svg
                                className="animate-spin h-5 w-5 mr-3 inline-block"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                stroke="currentColor"
                            >
                                <circle cx="12" cy="12" r="10" strokeWidth="4"></circle>
                                <path d="M12 2v4m6.36 1.64l-2.83 2.83M18 12h-4m-1.64 6.36l-2.83-2.83M12 22v-4m-6.36-1.64l2.83-2.83M6 12H2m1.64-6.36l2.83 2.83" strokeWidth="4"></path>
                            </svg>
                        ) : (
                            'Generate Reels'
                        )}
                    </button>
                </form>

                {reels.length > 0 && (
                    <div className="mt-8">
                        <h3 className="text-xl font-bold mb-4 text-center">Download Your Reels</h3>
                        <ul className="space-y-2">
                            {reels.map((reel, index) => (
                                <li key={index}>
                                    <a
                                        href={`${API_BASE_URL}/download-reel/${reel.reel_filename}`}
                                        download
                                        className="block w-full text-center bg-green-500 text-white py-2 rounded hover:bg-green-600"
                                    >
                                        {`Download Reel ${index + 1}`}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Form;
