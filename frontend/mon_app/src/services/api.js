import axios from 'axios';

// On pointe vers le port 8000 du backend
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getOffers = async () => {
  try {
    const response = await api.get('/offers');
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des offres:", error);
    throw error;
  }
};

export default api;

