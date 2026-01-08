// src/pages/Offers.jsx
import { useEffect, useState } from 'react';
import { getOffers } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Offers() {
  const [offres, setOffres] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchOffers = async () => {
      try {
        const data = await getOffers();
        setOffres(data);
      } catch (error) {
        console.error("Impossible de charger les offres");
      } finally {
        setLoading(false);
      }
    };
    fetchOffers();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex items-center justify-center">
        <div className="text-2xl font-bold text-blue-600">Chargement des offres...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-purple-100 py-16 px-4">
      <div className="container mx-auto max-w-7xl">
        
        {/* En-tête */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-black text-blue-600 mb-4">
            Nos Offres Olympiques
          </h1>
          <p className="text-xl text-gray-700 font-semibold">
            Choisissez l'offre adaptée à votre groupe
          </p>
        </div>
        
        {/* Grille des offres */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {offres.map((offre) => (
            <div
              key={offre.id}
              className="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-8 border-4 border-blue-600 hover:scale-105 transition-all duration-300"
            >
              {/* Nom de l'offre */}
              <div className="text-center mb-6">
                <h2 className="text-4xl font-black text-blue-600 mb-3">
                  {offre.nom_offre}
                </h2>
                <p className="text-gray-600 font-medium text-sm">
                  {offre.description}
                </p>
              </div>
              
              {/* Prix */}
              <div className="text-center mb-8">
                <div className="text-6xl font-black text-gray-900 mb-2">
                  {offre.prix} €
                </div>
                <p className="text-gray-600 font-semibold">
                  Pour {offre.capacite_personne} personne(s)
                </p>
              </div>
              
              {/* Bouton */}
              <button
                onClick={() => {
                  if (!isAuthenticated) {
                    alert('Veuillez vous connecter pour ajouter au panier');
                    return;
                  }
                  alert(`Offre ${offre.nom_offre} ajoutée au panier !`);
                }}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-black py-4 rounded-2xl hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 shadow-lg"
              >
                Ajouter au panier
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
            