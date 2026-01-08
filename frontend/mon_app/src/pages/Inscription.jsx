import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Inscription() {
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(formData.email, formData.nom, formData.prenom, formData.password);
      alert('Compte créé avec succès ! Vous pouvez maintenant vous connecter.');
      navigate('/connexion');
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création du compte');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-blue-100 to-purple-100 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Carte d'inscription */}
        <div className="bg-gradient-to-r from-amber-50 via-orange-50 to-yellow-50 rounded-3xl shadow-2xl p-10 border-4 border-blue-600">
          {/* Titre */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-black text-blue-600 mb-2">Inscription</h1>
            <p className="text-gray-600 font-medium">Créez votre compte JO 2024</p>
          </div>

          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Nom */}
            <div>
              <input
                type="text"
                name="nom"
                placeholder="Nom"
                value={formData.nom}
                onChange={handleChange}
                required
                className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-600 transition text-gray-800 placeholder-gray-400"
              />
            </div>

            {/* Prénom */}
            <div>
              <input
                type="text"
                name="prenom"
                placeholder="Prénom"
                value={formData.prenom}
                onChange={handleChange}
                required
                className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-600 transition text-gray-800 placeholder-gray-400"
              />
            </div>

            {/* Email */}
            <div>
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-600 transition text-gray-800 placeholder-gray-400"
              />
            </div>

            {/* Mot de passe */}
            <div>
              <input
                type="password"
                name="password"
                placeholder="Mot de passe"
                value={formData.password}
                onChange={handleChange}
                required
                minLength={6}
                className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-600 transition text-gray-800 placeholder-gray-400"
              />
            </div>

            {/* Message d'erreur */}
            {error && (
              <div className="bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded-2xl text-sm font-semibold">
                {error}
              </div>
            )}

            {/* Bouton d'inscription */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-black py-4 rounded-2xl hover:from-blue-700 hover:to-purple-700 transition transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Création...' : "S'inscrire"}
            </button>
          </form>

          {/* Lien connexion */}
          <div className="text-center mt-8">
            <p className="text-gray-600 font-medium">
              Déjà un compte ?{' '}
              <Link to="/connexion" className="text-blue-600 font-bold hover:text-blue-800 underline">
                Se connecter
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

