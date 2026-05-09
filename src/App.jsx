import React, { useState, useEffect } from 'react';
import CompanyCard from './components/CompanyCard';
import PMBriefModal from './components/PMBriefModal';
import Onboarding from './components/Onboarding';

function App() {
  localStorage.removeItem('userLens');
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState(null);
  
  // Lens state
  const [userLens, setUserLens] = useState(() => {
    const saved = localStorage.getItem('userLens');
    return saved ? JSON.parse(saved) : null;
  });
  
  // Theme toggle state
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Check initial preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove('dark');
    }
  }, []);

  useEffect(() => {
    if (!userLens) return;

    setLoading(true);
    const fileName = userLens ? `/data/${userLens.id}_signals.json` : '/data/social_signals.json';
    
    fetch(fileName)
      .then(res => {
         // Fallback to social_signals.json if the specific file hasn't been generated yet
         if (!res.ok) return fetch(`${import.meta.env.BASE_URL}data/social_signals.json`).then(r => r.json());
         return res.json();
      })
      .then(data => {
        setSignals(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load signals:", err);
        setLoading(false);
      });
  }, [userLens]);

  const toggleTheme = () => {
    const newDarkState = !isDarkMode;
    setIsDarkMode(newDarkState);
    if (newDarkState) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  const handleResetPersona = () => {
    localStorage.removeItem('userLens');
    setUserLens(null);
  };

  const handleGenerateBrief = (signal) => {
    setSelectedSignal(signal);
  };

  const handleCloseModal = () => {
    setSelectedSignal(null);
  };

  return (
    <>
      {!userLens ? (
        <Onboarding onComplete={setUserLens} />
      ) : (
        <div className="relative min-h-screen text-retro-ink dark:text-retro-paper transition-colors duration-500 z-0 p-8 sm:p-12 font-sans selection:bg-black selection:text-white dark:selection:bg-white dark:selection:text-black">
          {/* Background Layer */}
          <div className="fixed inset-0 z-[-2] bg-[#E5DED3] dark:bg-[#050505] overflow-hidden transition-colors duration-500">
          {/* Light Mode Blobs - Richer, darker beige/taupe tones */}
          <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#D4C8B2]/80 rounded-full blur-[120px] dark:opacity-0 transition-opacity duration-500"></div>
          <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] bg-[#C5B79F]/70 rounded-full blur-[140px] dark:opacity-0 transition-opacity duration-500"></div>
          <div className="absolute top-[20%] right-[10%] w-[40vw] h-[40vw] bg-[#B8A78D]/60 rounded-full blur-[100px] dark:opacity-0 transition-opacity duration-500"></div>

          {/* Dark Mode Blobs - Deep, subtle contrast */}
          <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#222222]/60 rounded-full blur-[120px] opacity-0 dark:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] bg-[#2D2D2D]/50 rounded-full blur-[140px] opacity-0 dark:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-[20%] right-[10%] w-[40vw] h-[40vw] bg-[#1A1A1A]/70 rounded-full blur-[100px] opacity-0 dark:opacity-100 transition-opacity duration-500"></div>
        </div>

        {/* Noise Texture Layer - Increased opacity for better visibility */}
        <div className="fixed inset-0 z-[-1] pointer-events-none bg-noise-texture opacity-[0.09] dark:opacity-[0.05] mix-blend-overlay"></div>
        {/* Top Right Controls */}
        <div className="fixed top-6 right-6 z-[999] flex items-center gap-3">
          {userLens && (
            <button 
              onClick={handleResetPersona}
              className="px-4 py-2 text-xs font-bold border-2 border-retro-ink dark:border-white/20 bg-retro-paper dark:bg-[#1A1A1A] shadow-retro dark:shadow-[4px_4px_0px_0px_rgba(255,255,255,0.1)] hover:-translate-y-1 hover:-translate-x-1 hover:shadow-retro-hover transition-all duration-200 rounded-none uppercase tracking-wider text-retro-ink dark:text-retro-paper"
            >
              Change Lens
            </button>
          )}
          <button 
            onClick={toggleTheme}
            className="bg-retro-paper dark:bg-retro-ink border-2 border-retro-ink dark:border-white/20 shadow-retro dark:shadow-retro-dark hover:-translate-y-1 hover:-translate-x-1 hover:shadow-retro-hover dark:hover:shadow-retro-dark-hover transition-all duration-300 rounded-none p-3"
            aria-label="Toggle dark mode"
          >
            {isDarkMode ? (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square" strokeLinejoin="miter">
                <circle cx="12" cy="12" r="5" />
                <line x1="12" y1="1" x2="12" y2="3" />
                <line x1="12" y1="21" x2="12" y2="23" />
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                <line x1="1" y1="12" x2="3" y2="12" />
                <line x1="21" y1="12" x2="23" y2="12" />
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
              </svg>
            ) : (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="square" strokeLinejoin="miter">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>
            )}
          </button>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="mb-8 pt-20 w-full z-10 relative">
            <h1 className="text-3xl font-bold font-mono uppercase tracking-tight text-black dark:text-[#F3F4F6]">Market Intelligence</h1>
            {userLens && (
              <p className="text-sm mt-1 text-black dark:text-gray-300 opacity-70">Lens: {userLens.name} • Tracking: {userLens.focus}</p>
            )}
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-64 border border-black dark:border-white/20 animate-pulse rounded-sm"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
              {signals.map((company) => (
                <CompanyCard
                  key={company.id}
                  company={company}
                  onGenerateBrief={() => handleGenerateBrief(company)}
                />
              ))}
            </div>
          )}

          <PMBriefModal
            isOpen={!!selectedSignal}
            onClose={handleCloseModal}
            brief={selectedSignal?.brief}
            metrics={selectedSignal?.metrics}
            companyName={selectedSignal?.ticker}
          />
        </div>
      </div>
      )}
    </>
  );
}

export default App;
