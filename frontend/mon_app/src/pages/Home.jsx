// src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const sports = [
    { nom: 'Athlétisme', slug: 'athletisme', color: 'bg-orange-500', emoji: '🏃‍♂️' },
    { nom: 'Natation', slug: 'natation', color: 'bg-blue-500', emoji: '🏊‍♂️' },
    { nom: 'BMX', slug: 'bmx', color: 'bg-yellow-500', emoji: '🚴‍♀️' },
    { nom: 'Boxe', slug: 'boxe', color: 'bg-red-500', emoji: '🥊' },
    { nom: 'Gymnastique', slug: 'gymnastique', color: 'bg-pink-500', emoji: '🤸‍♀️' },
    { nom: 'Escalade', slug: 'escalade', color: 'bg-green-500', emoji: '🧗‍♂️' },
  ];

  return (
    <div className="min-h-screen bg-[#0066FF] relative overflow-hidden">
      {/* Hero Section - Typographie géante */}
      <section className="min-h-screen flex items-center justify-center px-8 pt-32 pb-20 relative">
        {/* Éléments décoratifs flottants */}
        <div className="absolute top-40 right-20 bg-[#FF6B35] text-white px-6 py-3 rounded-full font-black text-sm transform rotate-6 animate-bounce">
          PARIS 2024
        </div>
        <div className="absolute bottom-40 left-20 bg-[#4ECB71] text-white px-6 py-3 rounded-full font-black text-sm transform -rotate-6">
          JEUX OLYMPIQUES
        </div>
        
        {/* Motif de points décoratifs */}
        <div className="absolute top-20 left-10 grid grid-cols-3 gap-4 opacity-20">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="w-4 h-4 bg-white rounded-full"></div>
          ))}
        </div>

        {/* Texte principal ultra-bold */}
        <div className="text-center relative z-10">
          <h1 className="font-black text-white leading-none mb-8" style={{fontSize: 'clamp(4rem, 15vw, 12rem)'}}>
            VIVEZ
            <br />
            <span className="relative inline-block">
              L'HISTOIRE
              <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 w-3/4 h-3 bg-yellow-400 rounded-full"></div>
            </span>
            <br />
            <span className="text-[#FFE66D]">OLYMPIQUE</span>
          </h1>
          
          <p className="text-white text-2xl md:text-3xl font-bold mb-12 max-w-3xl mx-auto">
            26 juillet - 11 août 2024 • Paris
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <Link
              to="/offres"
              className="bg-white text-[#0066FF] font-black px-10 py-5 rounded-full text-xl hover:bg-yellow-400 hover:text-gray-900 transition-all transform hover:scale-105 shadow-2xl"
            >
              Réserver mes billets →
            </Link>
            <Link
              to="/billetterie"
              className="border-4 border-white text-white font-black px-10 py-5 rounded-full text-xl hover:bg-white hover:text-[#0066FF] transition-all"
            >
              Découvrir
            </Link>
          </div>
        </div>

        {/* Illustration anneaux olympiques stylisés (côté) */}
        <div className="hidden lg:block absolute right-20 top-1/2 -translate-y-1/2">
          <svg width="300" height="200" viewBox="0 0 300 200" className="opacity-30">
            <circle cx="60" cy="80" r="40" fill="none" stroke="white" strokeWidth="8"/>
            <circle cx="150" cy="80" r="40" fill="none" stroke="#FFE66D" strokeWidth="8"/>
            <circle cx="240" cy="80" r="40" fill="none" stroke="white" strokeWidth="8"/>
            <circle cx="105" cy="130" r="40" fill="none" stroke="#4ECB71" strokeWidth="8"/>
            <circle cx="195" cy="130" r="40" fill="none" stroke="#FF6B35" strokeWidth="8"/>
          </svg>
        </div>
      </section>

      {/* Section Sports - Cards colorées */}
      <section className="bg-white rounded-t-[80px] py-20 px-8">
        <div className="max-w-7xl mx-auto">
          {/* En-tête section */}
          <div className="text-center mb-16">
            <div className="inline-block bg-blue-100 text-[#0066FF] px-6 py-3 rounded-full font-black mb-6">
              NOS ÉPREUVES
            </div>
            <h2 className="font-black text-gray-900 leading-tight mb-6" style={{fontSize: 'clamp(2.5rem, 8vw, 5rem)'}}>
              LES SPORTS
              <br />
              QUI VOUS ATTENDENT
            </h2>
            <p className="text-gray-600 text-xl max-w-2xl mx-auto">
              Découvrez les 6 disciplines phares et réservez vos places pour assister aux plus grandes performances
            </p>
          </div>

          {/* Grille de sports avec LIENS */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {sports.map((sport, index) => (
              <div
                key={index}
                className={`${sport.color} rounded-3xl p-8 text-white hover:scale-105 transition-transform shadow-xl`}
              >
                <div className="text-7xl mb-4">{sport.emoji}</div>
                <h3 className="font-black text-3xl mb-4">{sport.nom}</h3>
                <p className="text-white/90 mb-6 font-medium">
                  Assistez aux performances exceptionnelles de nos athlètes dans cette discipline olympique.
                </p>
                
                {/* Bouton avec lien vers /sport/{slug} */}
                <Link
                  to={`/sport/${sport.slug}`}
                  className="inline-block bg-white/20 backdrop-blur-sm border-2 border-white text-white font-bold px-6 py-3 rounded-full hover:bg-white hover:text-gray-900 transition-all"
                >
                  En savoir plus →
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Section CTA finale */}
      <section className="bg-white py-20 px-8">
        <div className="max-w-5xl mx-auto bg-gradient-to-r from-[#0066FF] to-purple-600 rounded-[60px] p-16 text-center text-white relative overflow-hidden">
          {/* Décoration */}
          <div className="absolute top-10 right-10 w-32 h-32 bg-yellow-400 rounded-full opacity-20 blur-2xl"></div>
          <div className="absolute bottom-10 left-10 w-40 h-40 bg-pink-500 rounded-full opacity-20 blur-2xl"></div>
          
          <div className="relative z-10">
            <h2 className="font-black text-5xl mb-6">
              NE RATEZ PAS L'ÉVÉNEMENT
              <br />
              DE LA DÉCENNIE
            </h2>
            <p className="text-2xl mb-10 text-blue-100">
              Offres Solo, Duo et Familiale disponibles dès maintenant
            </p>
            <Link
              to="/offres"
              className="inline-block bg-white text-[#0066FF] font-black px-12 py-6 rounded-full text-xl hover:bg-yellow-400 transition-all transform hover:scale-105 shadow-2xl"
            >
              Voir les offres →
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
            