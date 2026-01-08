import { useState, useEffect } from 'react';
import { sportsAPI } from '../services/api';
import SportCard from '../components/SportCard';

export default function Billetterie() {
  const [sports, setSports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadSports();
  }, []);

  const loadSports = async () => {
    try {
      const data = await sportsAPI.getAll();
      setSports(data);
    } catch (error) {
      console.error('Erreur chargement sports:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredSports = sports.filter(sport =>
    sport.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sport.lieu.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-2xl font-semibold text-gray-600">Chargement des sports...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        
        {/* En-tête */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-blue-600 mb-4">Billetterie Paris 2024</h1>
          <p className="text-xl text-gray-700">
            Réservez vos places pour les Jeux Olympiques de Paris
          </p>
        </div>

        {/* Barre de recherche */}
        <div className="max-w-2xl mx-auto mb-12">
          <input
            type="text"
            placeholder="Rechercher un sport ou un lieu..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-full focus:outline-none focus:border-blue-600 shadow-md"
          />
        </div>

        {/* Résultats */}
        {filteredSports.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-500">Aucun sport trouvé pour "{searchTerm}"</p>
          </div>
        ) : (
          <>
            <p className="text-center text-gray-600 mb-8">
              {filteredSports.length} sport{filteredSports.length > 1 ? 's' : ''} disponible{filteredSports.length > 1 ? 's' : ''}
            </p>
            
            {/* Grille de sports */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredSports.map(sport => (
                <SportCard key={sport.id} sport={sport} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

