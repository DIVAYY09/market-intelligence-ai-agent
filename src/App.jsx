import React, { useState, useEffect } from 'react';
import CompanyCard from './components/CompanyCard';
import PMBriefModal from './components/PMBriefModal';

function App() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSignal, setSelectedSignal] = useState(null);

  useEffect(() => {
    fetch('/data/social_signals.json')
      .then(res => res.json())
      .then(data => {
        setSignals(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load signals:", err);
        setLoading(false);
      });
  }, []);

  const handleGenerateBrief = (signal) => {
    setSelectedSignal(signal);
  };

  const handleCloseModal = () => {
    setSelectedSignal(null);
  };

  return (
    <div className="min-h-screen text-gray-100 p-8 sm:p-12 font-sans selection:bg-amber-500/30">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 flex items-end justify-between">
          <div>
            <h1 className="text-4xl font-bold tracking-tight text-white mb-2 drop-shadow-lg">
              Market Intelligence
            </h1>
            <p className="text-gray-400 text-lg">Daily signals and critical updates.</p>
          </div>
          <div className="hidden sm:block">
            <span className="text-sm font-medium text-gray-500 bg-white/5 py-1 px-3 rounded-full border border-white/5">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
            </span>
          </div>
        </header>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-64 bg-white/5 rounded-xl border border-white/5"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
  );
}

export default App;
