import React from 'react';
import { ExternalLink } from 'lucide-react';

const CompanyCard = ({ company, onGenerateBrief }) => {
    const isRelevant = company.relevant;

    return (
        <div
            onClick={onGenerateBrief}
            className={`
        relative p-6 rounded-sm transition-all duration-300 ease-out group cursor-pointer
        border border-black dark:border-white/20 bg-transparent
        hover:-translate-y-2 hover:-translate-x-1 hover:shadow-retro-hover dark:hover:shadow-retro-dark-hover
        ${isRelevant
                    ? 'border-2 hover:bg-white dark:hover:bg-[#F4F0EB]/10'
                    : 'hover:bg-white dark:hover:bg-[#F4F0EB]/10'
                }
      `}
        >
            <div className="flex flex-wrap items-center justify-between gap-2 mb-4 w-full">
                <span className="bg-retro-ink text-retro-paper dark:bg-[#2A2A2A] dark:text-[#E5E5E5] font-bold px-3 py-1 text-xs uppercase tracking-widest border border-transparent dark:border-white/10 rounded-full">{company.time}</span>
                {isRelevant && (
                    <div className="p-[1px] bg-black dark:bg-[#2A2A2A] rounded-sm shrink-0 border border-transparent dark:border-white/10">
                        <div className="px-3 py-1 bg-black dark:bg-transparent flex items-center gap-1.5">
                            <span className="relative flex h-2 w-2">
                                <span className="relative inline-flex h-2 w-2 bg-white dark:bg-[#E5E5E5]"></span>
                            </span>
                            <span className="text-[10px] font-bold text-white dark:text-[#E5E5E5] tracking-wider uppercase">High Signal</span>
                        </div>
                    </div>
                )}
            </div>

            <div className="mb-4">
                <span className="text-xs font-bold uppercase tracking-wider inherit-text block">{company.ticker}</span>
                <h3 className="text-lg font-bold mt-1 leading-snug inherit-text">
                    {company.name}
                </h3>
            </div>

            <div className="space-y-4">
                <div>
                    <p className="text-sm leading-relaxed font-normal inherit-text">
                        {company.signal}
                    </p>
                </div>

                <div className="pt-4 flex items-center justify-between border-t border-black dark:border-white/20 group-hover:border-white dark:group-hover:border-white/20">
                    <span className={`
            text-xs px-2.5 py-1 rounded-sm font-bold border border-black dark:border-white/20
            ${company.sentiment === 'positive' ? 'bg-transparent text-inherit' :
                            company.sentiment === 'negative' ? 'bg-transparent text-inherit' :
                                'bg-transparent text-inherit'}
          `}>
                        {company.sentiment.charAt(0).toUpperCase() + company.sentiment.slice(1)}
                    </span>

                    <div className="flex items-center gap-3">
                        <a
                            href={company.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="text-xs font-bold flex items-center gap-1.5 border border-transparent hover:border-current px-2 py-1 transition-none"
                        >
                            Read Original
                            <ExternalLink className="w-3 h-3" />
                        </a>
                        <button
                            onClick={(e) => {
                                e.stopPropagation();
                                onGenerateBrief();
                            }}
                            className="text-xs font-bold flex items-center gap-1 border border-black dark:border-white/20 px-2 py-1 bg-transparent text-black dark:text-[#E5E5E5] hover:bg-black hover:text-white dark:hover:bg-[#E5E5E5] dark:hover:text-[#121212] transition-none rounded-sm z-10 relative"
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
