
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { billetsAPI, panierAPI } from '../services/api';

export default function Profil() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('billets');
  const [billets, setBillets] = useState([]);
  const [panier, setPanier] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fonction loadUserData avec useCallback pour éviter les warnings
  const loadUserData = useCallback(async () => {
    try {
      setLoading(true);
      // Charger les billets achetés
      const billetsData = await billetsAPI.getUserBillets(user.id);
      setBillets(billetsData);

      // Charger le panier
      const panierData = await panierAPI.getItems(user.id);
      setPanier(panierData);
    } catch (error) {
      console.error('Erreur chargement données:', error);
    } finally {
      setLoading(false);
    }
  }, [user.id]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/connexion');
      return;
    }

    loadUserData();
  }, [isAuthenticated, navigate, loadUserData]);

  const handleDeleteFromPanier = async (itemId) => {
    if (!window.confirm('Supprimer cet article du panier ?')) return;

    try {
      await panierAPI.supprimer(user.id, itemId);
      setPanier(panier.filter(item => item.id !== itemId));
    } catch (error) {
      alert('Erreur lors de la suppression');
    }
  };

  const handleValiderPanier = async () => {
    if (panier.length === 0) {
      alert('Votre panier est vide');
      return;
    }

    if (!window.confirm(`Confirmer l'achat de ${panier.length} article(s) ?`)) return;

    try {
      await panierAPI.valider(user.id);
      alert('Commande validée avec succès !');
      loadUserData(); // Recharger les données
    } catch (error) {
      alert('Erreur lors de la validation du panier');
    }
  };

  const handleDownloadPDF = async (billetId) => {
    try {
      console.log(`📥 Téléchargement du billet ${billetId}...`);
      
      const token = localStorage.getItem('token');
      
      const response = await 
      fetch(`${process.env.REACT_APP_API_URL}/api/tickets/${billetId}/download-pdf`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      // Récupérer le blob PDF
      const blob = await response.blob();

      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `billet_paris2024_${billetId}.pdf`;
      
      // Télécharger
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Libérer la mémoire
      window.URL.revokeObjectURL(url);
      
      console.log('✅ PDF téléchargé avec succès');
    } catch (error) {
      console.error('❌ Erreur lors du téléchargement:', error);
      alert('Erreur lors du téléchargement du billet. Veuillez réessayer.');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!isAuthenticated) {
    return null;
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex items-center justify-center">
        <div className="text-2xl font-bold text-blue-600">Chargement du profil...</div>
      </div>
    );
  }

  // Calculer le total du panier
  const totalPanier = panier.reduce((sum, item) => sum + (item.prix_total || 0), 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-purple-100 py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        
        {/* Header Profil */}
        <div className="bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-8 mb-8 border-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              {/* Avatar avec initiales */}
              <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center text-white text-3xl font-black">
                {user.prenom?.charAt(0)}{user.nom?.charAt(0)}
              </div>
              
              {/* Info utilisateur */}
              <div>
                <h1 className="text-4xl font-black text-blue-600 mb-2">
                  {user.prenom} {user.nom}
                </h1>
                <p className="text-gray-600 font-medium text-lg">{user.email}</p>
              </div>
            </div>

            {/* Bouton déconnexion */}
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white font-bold px-6 py-3 rounded-full hover:bg-red-600 transition"
            >
              Déconnexion
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('billets')}
            className={`flex-1 py-4 rounded-2xl font-black text-xl transition ${
              activeTab === 'billets'
                ? 'bg-blue-600 text-white shadow-xl'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            }`}
          >
            Mes Billets ({billets.length})
          </button>
          <button
            onClick={() => setActiveTab('panier')}
            className={`flex-1 py-4 rounded-2xl font-black text-xl transition ${
              activeTab === 'panier'
                ? 'bg-blue-600 text-white shadow-xl'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            }`}
          >
            Mon Panier ({panier.length})
          </button>
        </div>

        {/* Contenu des tabs */}
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          
          {/* Tab Mes Billets */}
          {activeTab === 'billets' && (
            <div>
              <h2 className="text-3xl font-black text-gray-900 mb-8">Mes Billets Achetés</h2>
              
              {billets.length === 0 ? (
                <div className="text-center py-16">
                  <div className="text-6xl mb-4">🎫</div>
                  <p className="text-xl text-gray-500 font-medium">
                    Vous n'avez pas encore acheté de billets
                  </p>
                  <button
                    onClick={() => navigate('/billetterie')}
                    className="mt-6 bg-blue-600 text-white font-bold px-8 py-4 rounded-full hover:bg-blue-700 transition"
                  >
                    Découvrir les événements
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {billets.map((billet) => (
                    <div
                      key={billet.id}
                      className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-blue-600 rounded-2xl p-6 hover:shadow-xl transition"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-2xl font-black text-blue-600 mb-3">
                            {billet.epreuve_nom || 'Épreuve'}
                          </h3>
                          
                          <div className="space-y-2 text-gray-700">
                            <div className="flex items-center gap-2">
                              <span className="text-xl">🏅</span>
                              <span className="font-semibold">{billet.sport_nom || 'Sport'}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xl">📍</span>
                              <span className="font-semibold">{billet.lieu || 'Lieu'}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xl">📅</span>
                              <span className="font-semibold">
                                {billet.date_epreuve 
                                  ? new Date(billet.date_epreuve).toLocaleDateString('fr-FR', {
                                      day: '2-digit',
                                      month: 'long',
                                      year: 'numeric'
                                    })
                                  : 'Date non spécifiée'
                                }
                                {billet.heure ? ` à ${billet.heure}` : ''}
                              </span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xl">🎟️</span>
                              <span className="font-semibold">
                                {billet.nombre_places} place(s) - {billet.offer_nom || 'Offre'}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="text-right">
                          <div className="text-4xl font-black text-green-600 mb-4">
                            {billet.prix_total}€
                          </div>
                          <button 
                            onClick={() => handleDownloadPDF(billet.id)}
                            className="bg-blue-600 text-white font-bold px-6 py-3 rounded-full hover:bg-blue-700 transition"
                          >
                            📥 Télécharger
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Tab Mon Panier */}
          {activeTab === 'panier' && (
            <div>
              <h2 className="text-3xl font-black text-gray-900 mb-8">Mon Panier</h2>
              
              {panier.length === 0 ? (
                <div className="text-center py-16">
                  <div className="text-6xl mb-4">🛒</div>
                  <p className="text-xl text-gray-500 font-medium">
                    Votre panier est vide
                  </p>
                  <button
                    onClick={() => navigate('/billetterie')}
                    className="mt-6 bg-blue-600 text-white font-bold px-8 py-4 rounded-full hover:bg-blue-700 transition"
                  >
                    Parcourir les événements
                  </button>
                </div>
              ) : (
                <>
                  <div className="space-y-6 mb-8">
                    {panier.map((item) => (
                      <div
                        key={item.id}
                        className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-blue-600 rounded-2xl p-6 hover:shadow-xl transition"
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="text-2xl font-black text-blue-600 mb-3">
                              {item.epreuve_nom || 'Épreuve'}
                            </h3>
                            
                            <div className="space-y-2 text-gray-700">
                              <div className="flex items-center gap-2">
                                <span className="text-xl">🏅</span>
                                <span className="font-semibold">{item.sport_nom || 'Sport'}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="text-xl">📅</span>
                                <span className="font-semibold">
                                  {item.date_epreuve ? new Date(item.date_epreuve).toLocaleDateString('fr-FR') : 'Date à venir'}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="text-xl">🎟️</span>
                                <span className="font-semibold">
                                  {item.nombre_places} place(s) - Offre {item.offer_nom}
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="text-right flex flex-col gap-4">
                            <div className="text-4xl font-black text-blue-600">
                              {item.prix_total}€
                            </div>
                            <button
                              onClick={() => handleDeleteFromPanier(item.id)}
                              className="bg-red-500 text-white font-bold px-6 py-3 rounded-full hover:bg-red-600 transition"
                            >
                              Supprimer
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Total et validation */}
                  <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-xl font-semibold mb-2">Total à payer</p>
                        <p className="text-5xl font-black">{totalPanier.toFixed(2)}€</p>
                      </div>
                      <button
                        onClick={handleValiderPanier}
                        className="bg-white text-blue-600 font-black px-12 py-5 rounded-full text-xl hover:bg-yellow-400 hover:text-gray-900 transition transform hover:scale-105 shadow-2xl"
                      >
                        Valider mon panier
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
