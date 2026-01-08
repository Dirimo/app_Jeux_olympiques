// src/components/Header.jsx
import { Link } from 'react-router-dom';
import OlympicRings from './OlympicRings';

export default function Header() {
  return (
    <header className="bg-blue-600 sticky top-0 z-50">
      {/* Conteneur avec bords arrondis */}
      <div className="bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 rounded-b-[60px] shadow-xl border-b-4 border-blue-600">
        <div className="container mx-auto px-8 py-5">
          <div className="flex items-center justify-between">
            
            {/* Logo + Anneaux */}
            <Link to="/" className="flex items-center gap-4 hover:opacity-80 transition">
              <OlympicRings className="w-16 h-10" />
              <h1 className="text-3xl font-black text-blue-600">
                PARIS 2024
              </h1>
            </Link>
            
            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-8">
              <Link 
                to="/" 
                className="text-blue-600 font-bold hover:text-blue-800 transition"
              >
                Accueil
              </Link>
              <Link 
                to="/billetterie" 
                className="text-blue-600 font-bold hover:text-blue-800 transition"
              >
                Billetterie
              </Link>
              <Link 
                to="/profil" 
                className="text-blue-600 font-bold hover:text-blue-800 transition"
              >
                Mon Profil
              </Link>
              <Link 
                to="/connexion" 
                className="bg-orange-500 text-white font-black px-8 py-3 rounded-full hover:bg-orange-600 transition shadow-lg transform hover:scale-105"
              >
                Connexion →
              </Link>
            </nav>

            {/* Menu mobile */}
            <button className="md:hidden text-blue-600">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
