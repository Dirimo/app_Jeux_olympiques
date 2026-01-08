// src/pages/SportDetail.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { sportsAPI, panierAPI, getOffers } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function SportDetail() {
  const { slug } = useParams();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [sport, setSport] = useState(null);
  const [epreuves, setEpreuves] = useState([]);
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedEpreuve, setSelectedEpreuve] = useState(null);
  const [selectedOffer, setSelectedOffer] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadSportData();
    loadOffers();
  }, [slug]);

  const loadSportData = async () => {
    try {
      const data = await sportsAPI.getBySlug(slug);
      setSport(data);
      setEpreuves(data.epreuves || []);
    } catch (error) {
      console.error('Erreur chargement sport:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadOffers = async () => {
    try {
      const data = await getOffers();
      setOffers(data);
    } catch (error) {
      console.error('Erreur chargement offres:', error);
    }
  };

  const handleReserver = (epreuve) => {
    if (!isAuthenticated) {
      alert('Veuillez vous connecter pour réserver');
      navigate('/connexion');
      return;
    }

    setSelectedEpreuve(epreuve);
    setShowModal(true);
  };

  const handleAddToPanier = async () => {
    if (!selectedOffer) {
      alert('Veuillez sélectionner une offre');
      return;
    }

    try {
      await panierAPI.ajouter(
        user.id,
        selectedEpreuve.id,
        selectedOffer.id,
        1 // nombre de places
      );
      alert('Ajouté au panier avec succès !');
      setShowModal(false);
      setSelectedOffer(null);
    } catch (error) {
      alert('Erreur lors de l\'ajout au panier');
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex items-center justify-center">
        <div className="text-2xl font-bold text-blue-600">Chargement...</div>
      </div>
    );
  }

  if (!sport) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-3xl font-black text-gray-800 mb-4">Sport non trouvé</h2>
          <button
            onClick={() => navigate('/billetterie')}
            className="bg-blue-600 text-white font-bold px-8 py-4 rounded-full hover:bg-blue-700 transition"
          >
            Retour à la billetterie
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-purple-100">
      
      {/* Hero Section */}
      <div className="relative h-96">
        <img 
          src={sport.image_url} 
          alt={sport.nom}
          className="w-full h-full object-cover"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/1200x400/0066FF/FFFFFF?text=' + sport.nom;
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-7xl font-black text-white drop-shadow-2xl">{sport.nom}</h1>
        </div>
      </div>

      {/* Contenu */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          
          {/* Colonne principale */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Histoire */}
            <div className="bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-8 border-4 border-blue-600">
              <h2 className="text-3xl font-black text-blue-600 mb-6">Histoire</h2>
              <p className="text-gray-800 leading-relaxed text-lg font-medium">
                {sport.histoire}
              </p>
            </div>

            {/* Épreuves disponibles */}
            <div className="bg-white rounded-3xl shadow-2xl p-8">
              <h2 className="text-3xl font-black text-blue-600 mb-8">
                Épreuves disponibles ({epreuves.length})
              </h2>
              
              {epreuves.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🏅</div>
                  <p className="text-xl text-gray-500 font-medium">
                    Aucune épreuve disponible pour le moment
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {epreuves.map((epreuve) => (
                    <div
                      key={epreuve.id}
                      className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-blue-600 rounded-2xl p-6 hover:shadow-xl transition"
                    >
                      <div className="flex justify-between items-start gap-4">
                        <div className="flex-1">
                          <h3 className="text-2xl font-black text-blue-600 mb-3">
                            {epreuve.nom_epreuve}
                          </h3>
                          
                          <div className="space-y-2 text-gray-700">
                            <div className="flex items-center gap-2">
                              <span className="text-xl">📅</span>
                              <span className="font-semibold">
                                {new Date(epreuve.date_epreuve).toLocaleDateString('fr-FR', {
                                  weekday: 'long',
                                  day: 'numeric',
                                  month: 'long',
                                  year: 'numeric'
                                })}
                              </span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xl">🕐</span>
                              <span className="font-semibold">{epreuve.heure}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xl">🎟️</span>
                              <span className="font-semibold">
                                {epreuve.places_disponibles} places disponibles
                              </span>
                            </div>
                          </div>
                        </div>

                        <button
                          onClick={() => handleReserver(epreuve)}
                          className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-black px-8 py-4 rounded-full hover:from-blue-700 hover:to-purple-700 transition transform hover:scale-105 shadow-lg"
                        >
                          Réserver →
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar Informations */}
          <div>
            <div className="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-8 border-4 border-blue-600 sticky top-4">
              <h3 className="text-2xl font-black text-blue-600 mb-6">Informations pratiques</h3>
              
              <div className="space-y-5 mb-8">
                <div className="flex items-start gap-3">
                  <span className="text-3xl">📍</span>
                  <div>
                    <p className="font-black text-gray-900">Lieu</p>
                    <p className="text-gray-700 font-semibold">{sport.lieu}</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <span className="text-3xl">📅</span>
                  <div>
                    <p className="font-black text-gray-900">Dates</p>
                    <p className="text-gray-700 font-semibold">{sport.dates_competition}</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <span className="text-3xl">🎫</span>
                  <div>
                    <p className="font-black text-gray-900">Épreuves</p>
                    <p className="text-gray-700 font-semibold">{epreuves.length} épreuve(s)</p>
                  </div>
                </div>
              </div>

              <button
                onClick={() => navigate('/billetterie')}
                className="w-full bg-white text-blue-600 border-2 border-blue-600 font-black py-4 rounded-2xl hover:bg-blue-600 hover:text-white transition"
              >
                ← Retour aux sports
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de sélection d'offre */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-8 max-w-2xl w-full border-4 border-blue-600 max-h-[90vh] overflow-y-auto">
            <h2 className="text-3xl font-black text-blue-600 mb-6">
              Choisissez votre offre
            </h2>

            <div className="mb-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {selectedEpreuve?.nom_epreuve}
              </h3>
              <p className="text-gray-700 font-medium">
                {new Date(selectedEpreuve?.date_epreuve).toLocaleDateString('fr-FR')} à {selectedEpreuve?.heure}
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-4 mb-8">
              {offers.map((offer) => (
                <div
                  key={offer.id}
                  onClick={() => setSelectedOffer(offer)}
                  className={`cursor-pointer rounded-2xl p-6 border-4 transition ${
                    selectedOffer?.id === offer.id
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-300 bg-white hover:border-blue-400'
                  }`}
                >
                  <h4 className="text-2xl font-black text-blue-600 mb-2">{offer.nom_offre}</h4>
                  <p className="text-sm text-gray-600 mb-4">{offer.description}</p>
                  <p className="text-4xl font-black text-gray-900">{offer.prix}€</p>
                  <p className="text-sm text-gray-500">Pour {offer.capacite_personne} pers.</p>
                </div>
              ))}
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => {
                  setShowModal(false);
                  setSelectedOffer(null);
                }}
                className="flex-1 bg-gray-300 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-400 transition"
              >
                Annuler
              </button>
              <button
                onClick={handleAddToPanier}
                disabled={!selectedOffer}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-black py-4 rounded-2xl hover:from-blue-700 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Ajouter au panier
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
