// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import Home from './pages/Home';
import Billetterie from './pages/Billetterie';
import Profil from './pages/Profil';
import SportDetail from './pages/SportDetail';
import Login from './pages/Login';
import Inscription from './pages/Inscription';
import Offers from './pages/Offers';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/billetterie" element={<Billetterie />} />
          <Route path="/profil" element={<Profil />} />
          <Route path="/sport/:slug" element={<SportDetail />} />
          <Route path="/connexion" element={<Login />} />
          <Route path="/inscription" element={<Inscription />} />
          <Route path="/offres" element={<Offers />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
