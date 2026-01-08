// src/context/AuthContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Charger l'utilisateur depuis localStorage au démarrage
    const currentUser = authAPI.getCurrentUser();
    console.log('User chargé depuis localStorage:', currentUser);  // ← Debug
    setUser(currentUser);
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const userData = await authAPI.login(email, password);
      console.log('Réponse API login dans AuthContext:', userData);  // ← Debug
      
      // ⚠️ VÉRIFIER QUE userData contient bien un id
      if (!userData || !userData.id) {
        console.error('ERREUR: userData.id est undefined', userData);
        throw new Error('ID utilisateur manquant dans la réponse API');
      }
      
      console.log('User.id défini:', userData.id);  // ← Debug
      setUser(userData);
      return userData;
    } catch (error) {
      console.error('Erreur de connexion:', error);
      throw error;
    }
  };

  const register = async (email, nom, prenom, password) => {
    try {
      const userData = await authAPI.register(email, nom, prenom, password);
      console.log('Réponse API register:', userData);  // ← Debug
      return userData;
    } catch (error) {
      console.error("Erreur d'inscription:", error);
      throw error;
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
