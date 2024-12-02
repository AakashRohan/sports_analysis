import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const fetchMatches = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/matches`);
    return response.data;
  } catch (error) {
    console.error('Error fetching matches:', error);
    throw error;
  }
};

export const fetchMatchDetails = async (matchId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/matches/${matchId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching match details:', error);
    throw error;
  }
};
