import React, { useState } from 'react';
import { PERSONAS } from '../data/personas';

const Onboarding = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [selectedRoleId, setSelectedRoleId] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);

  const selectedRole = PERSONAS.find(p => p.id === selectedRoleId);

  const handleRoleSelect = (roleId) => {
    setSelectedRoleId(roleId);
    setStep(2);
  };

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };

  const handleInitialize = () => {
    if (!selectedRoleId || !selectedOption) return;
    const lens = { id: selectedRole.id, name: selectedRole.role, focus: selectedOption };
    localStorage.setItem('userLens', JSON.stringify(lens));
    onComplete(lens);
  };

  return (
    <div className="fixed inset-0 z-50 bg-[#E5DED3] dark:bg-[#050505] flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-retro-paper dark:bg-retro-ink border-4 border-retro-ink dark:border-retro-paper p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_0px_rgba(255,255,255,1)]">
        {step === 1 ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-3xl md:text-4xl font-bold mb-8 text-black dark:text-white uppercase tracking-tighter">
              Select your primary role:
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {PERSONAS.map((persona) => (
                <button
                  key={persona.id}
                  onClick={() => handleRoleSelect(persona.id)}
                  className="p-4 text-left border-2 border-black dark:border-white bg-white dark:bg-black text-black dark:text-white hover:-translate-y-1 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] transition-all font-medium text-lg"
                >
                  {persona.role}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="animate-in fade-in slide-in-from-right-8 duration-500">
            <h2 className="text-3xl md:text-4xl font-bold mb-8 text-black dark:text-white uppercase tracking-tighter">
              What do you want to track?
            </h2>
            <div className="flex flex-col gap-4 mb-8">
              {selectedRole?.options.map((option, idx) => (
                <button
                  key={idx}
                  onClick={() => handleOptionSelect(option)}
                  className={`p-4 text-left border-2 border-black dark:border-white transition-all font-medium text-lg ${
                    selectedOption === option
                      ? 'bg-black text-white dark:bg-white dark:text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] translate-x-2'
                      : 'bg-white text-black dark:bg-black dark:text-white hover:-translate-y-1 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)]'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
            
            <div className="flex justify-between items-center mt-8 pt-6 border-t-2 border-black dark:border-white">
              <button 
                onClick={() => {
                  setStep(1);
                  setSelectedOption(null);
                }}
                className="text-black dark:text-white underline font-bold hover:opacity-70 transition-opacity"
              >
                ← Back
              </button>
              
              <button
                onClick={handleInitialize}
                disabled={!selectedOption}
                className="px-8 py-3 bg-black text-white dark:bg-white dark:text-black border-2 border-transparent hover:bg-transparent hover:text-black hover:border-black dark:hover:text-white dark:hover:border-white disabled:opacity-50 disabled:cursor-not-allowed transition-all font-bold uppercase tracking-wider text-lg"
              >
                Initialize Dashboard
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Onboarding;
