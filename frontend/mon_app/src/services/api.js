import axios from 'axios';

// On pointe vers le port 8000 du backend
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== OFFERS ====================

export const getOffers = async () => {
  try {
    const response = await api.get('/offers');
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des offres:", error);
    throw error;
  }
};

// ==================== AUTH ====================

export const authAPI = {
  register: async (email, nom, prenom, password) => {
    try {
      const response = await api.post('/api/auth/register', null, {
        params: { email, nom, prenom, password }
      });
      console.log('✅ Inscription réussie:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de l'inscription:", error);
      throw error;
    }
  },
  
  login: async (email, password) => {
    try {
      console.log('🔐 Tentative de connexion:', { email });
      
      const response = await api.post('/api/auth/login', null, {
        params: { email, password }
      });
      
      console.log('✅ Réponse API login:', response.data);
      
      if (!response.data || !response.data.id) {
        console.error('❌ ERREUR: Pas d\'id dans response.data', response.data);
        throw new Error('ID utilisateur manquant dans la réponse API');
      }
      
      console.log('✅ User.id trouvé:', response.data.id);
      
      localStorage.setItem('user', JSON.stringify(response.data));
      console.log('✅ User sauvegardé dans localStorage:', response.data);
      
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de la connexion:", error);
      if (error.response) {
        console.error("Détails de l'erreur:", error.response.data);
      }
      throw error;
    }
  },
  
  logout: () => {
    localStorage.removeItem('user');
    console.log('✅ Déconnexion - User supprimé de localStorage');
  },
  
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      console.log('ℹ️ Aucun user dans localStorage');
      return null;
    }
    
    try {
      const user = JSON.parse(userStr);
      console.log('✅ getCurrentUser:', user);
      
      if (!user.id) {
        console.error('❌ ERREUR: user.id est undefined dans localStorage', user);
        localStorage.removeItem('user');
        return null;
      }
      
      return user;
    } catch (error) {
      console.error('❌ Erreur parsing user depuis localStorage:', error);
      localStorage.removeItem('user');
      return null;
    }
  }
};

// ==================== SPORTS ====================

export const sportsAPI = {
  getAll: async () => {
    try {
      const response = await api.get('/api/sports');
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des sports:", error);
      throw error;
    }
  },
  
  getBySlug: async (slug) => {
    try {
      const response = await api.get(`/api/sports/${slug}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération du sport ${slug}:`, error);
      throw error;
    }
  }
};

// ==================== BILLETS ====================

export const billetsAPI = {
  getUserBillets: async (userId) => {
    try {
      console.log('🎫 Récupération billets pour userId:', userId);
      
      if (!userId || userId === 'undefined') {
        console.error('❌ ERREUR: userId invalide', userId);
        throw new Error('User ID invalide');
      }
      
      const response = await api.get(`/api/tickets/user/${userId}`);
      console.log('✅ Billets récupérés:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de la récupération des billets:", error);
      throw error;
    }
  }
};

// ==================== PANIER ====================

export const panierAPI = {
  getItems: async (userId) => {
    try {
      console.log('🛒 Récupération panier pour userId:', userId);
      
      if (!userId || userId === 'undefined') {
        console.error('❌ ERREUR: userId invalide', userId);
        return []; // Retourner tableau vide au lieu de throw
      }
      
      const response = await api.get(`/api/panier/user/${userId}`);
      console.log('✅ Panier récupéré:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de la récupération du panier:", error);
      return []; // Retourner tableau vide en cas d'erreur
    }
  },
  
  ajouter: async (userId, epreuveId, offerId, nombrePlaces = 1) => {
    try {
      console.log('🛒 Ajout au panier:', { userId, epreuveId, offerId, nombrePlaces });
      
      if (!userId || userId === 'undefined') {
        console.error('❌ ERREUR: userId invalide', userId);
        throw new Error('User ID invalide - Veuillez vous connecter');
      }
      
      const response = await api.post(`/api/panier/user/${userId}`, null, {
        params: {
          epreuve_id: epreuveId,
          offer_id: offerId,
          nombre_places: nombrePlaces
        }
      });
      
      console.log('✅ Ajout au panier réussi:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de l'ajout au panier:", error);
      if (error.response) {
        console.error("Détails de l'erreur:", error.response.data);
      }
      throw error;
    }
  },
  
  supprimer: async (userId, itemId) => {
    try {
      console.log('🗑️ Suppression item:', { userId, itemId });
      
      if (!userId || userId === 'undefined') {
        console.error('❌ ERREUR: userId invalide', userId);
        throw new Error('User ID invalide');
      }
      
      const response = await api.delete(`/api/panier/user/${userId}/item/${itemId}`);
      console.log('✅ Suppression réussie:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de la suppression du panier:", error);
      throw error;
    }
  },
  
  valider: async (userId) => {
    try {
      console.log('✅ Validation panier pour userId:', userId);
      
      if (!userId || userId === 'undefined') {
        console.error('❌ ERREUR: userId invalide', userId);
        throw new Error('User ID invalide');
      }
      
      const response = await api.post(`/api/panier/user/${userId}/valider`);
      console.log('✅ Validation réussie:', response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Erreur lors de la validation du panier:", error);
      if (error.response) {
        console.error("Détails de l'erreur:", error.response.data);
      }
      throw error;
    }
  }
};

export default api;

