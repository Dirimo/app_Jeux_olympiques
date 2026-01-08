import { Link } from 'react-router-dom';

export default function SportCard({ sport }) {
  return (
    <Link 
      to={`/sport/${sport.slug}`}
      className="group block bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-2"
    >
      {/* Image */}
      <div className="relative h-64 overflow-hidden">
        <img 
          src={sport.image_url} 
          alt={sport.nom}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
        
        {/* Nom du sport */}
        <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
          <h3 className="text-3xl font-bold mb-2">{sport.nom}</h3>
        </div>
      </div>

      {/* Infos */}
      <div className="p-6">
        <p className="text-gray-700 mb-4 line-clamp-2">{sport.description}</p>
        
        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-gray-600">
            <span className="text-xl">📍</span>
            <span className="text-sm font-medium">{sport.lieu}</span>
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <span className="text-xl">📅</span>
            <span className="text-sm font-medium">{sport.dates_competition}</span>
          </div>
        </div>

        {/* Bouton */}
        <div className="flex items-center justify-between">
          <span className="text-blue-600 font-bold group-hover:text-blue-700 transition">
            Voir les épreuves →
          </span>
        </div>
      </div>
    </Link>
  );
}
