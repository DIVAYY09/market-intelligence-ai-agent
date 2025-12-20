import React from 'react';
import { ExternalLink } from 'lucide-react';

const CompanyCard = ({ company, onGenerateBrief }) => {
    const isRelevant = company.relevant;

    return (
        <div
            className={`
        relative p-6 rounded-xl transition-all duration-300 group
        backdrop-blur-md border 
        ${isRelevant
                    ? 'bg-amber-900/10 border-amber-500/30 shadow-[0_0_20px_-5px_rgba(245,158,11,0.2)] hover:shadow-[0_0_30px_-5px_rgba(245,158,11,0.3)] hover:border-amber-500/50'
                    : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20 hover:shadow-lg'
                }
      `}
        >
            {isRelevant && (
                <div className="absolute top-0 right-0 p-[1px] rounded-bl-xl rounded-tr-xl bg-gradient-to-l from-amber-500/50 to-transparent">
                    <div className="px-3 py-1 bg-slate-900/80 backdrop-blur-sm rounded-bl-xl rounded-tr-xl border-l border-b border-amber-500/20 flex items-center gap-1.5">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                        </span>
                        <span className="text-[10px] font-bold text-amber-500 tracking-wider uppercase">High Signal</span>
                    </div>
                </div>
            )}

            <div className="mb-4">
                <div className="flex justify-between items-start">
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">{company.ticker}</span>
                    <span className="text-xs text-gray-600">{company.time}</span>
                </div>
                <h3 className="text-lg font-semibold text-white mt-1 leading-snug group-hover:text-amber-100 transition-colors">
                    {company.name}
                </h3>
            </div>

            <div className="space-y-4">
                <div>
                    <p className="text-sm text-gray-300 leading-relaxed font-light">
                        {company.signal}
                    </p>
                </div>

                <div className="pt-4 flex items-center justify-between border-t border-white/5">
                    <span className={`
            text-xs px-2.5 py-1 rounded-md font-medium border
            ${company.sentiment === 'positive' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                            company.sentiment === 'negative' ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' :
                                'bg-slate-700/50 text-slate-400 border-slate-600/50'}
          `}>
                        {company.sentiment.charAt(0).toUpperCase() + company.sentiment.slice(1)}
                    </span>

                    <div className="flex items-center gap-3">
                        <a
                            href={company.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs font-medium text-gray-500 hover:text-white flex items-center gap-1.5 transition-colors"
                        >
                            Read Original
                            <ExternalLink className="w-3 h-3" />
                        </a>
                        <button
                            onClick={onGenerateBrief}
                            className="text-xs font-semibold text-amber-400 hover:text-amber-300 transition-colors flex items-center gap-1"
                        >
                            Generate Brief
                            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CompanyCard;
