import React from 'react';

const PMBriefModal = ({ isOpen, onClose, brief, metrics, companyName }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/80 transition-none"
                onClick={onClose}
            ></div>

            {/* Modal Content */}
            <div className="relative w-full max-w-2xl bg-retro-surface dark:bg-retro-dark-surface border-2 border-retro-ink dark:border-white/20 shadow-[8px_8px_0px_0px_rgba(26,26,26,1)] dark:shadow-[8px_8px_0px_0px_rgba(240,235,225,1)] rounded-none overflow-hidden transform transition-none">
                {/* Header */}
                <div className="bg-transparent px-6 py-4 border-b-2 border-black dark:border-white/20 flex items-center justify-between">
                    <h3 className="text-xl font-bold text-black dark:text-[#F3F4F6] tracking-tight">
                        PM Brief: {companyName}
                    </h3>
                    <button
                        onClick={onClose}
                        className="text-black dark:text-[#F3F4F6] border-2 border-black dark:border-white/20 hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition-colors duration-200 p-2 font-mono font-bold"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Body */}
                <div className="p-6 space-y-6">
                    {/* Brief Text */}
                    <div className="prose max-w-none text-black dark:text-[#D4D4D4]">
                        <h4 className="text-black dark:text-[#F3F4F6] text-sm font-bold uppercase tracking-wider mb-2">Executive Summary</h4>
                        <p className="text-black dark:text-[#D4D4D4] leading-relaxed text-base">
                            {brief || "No brief available for this signal. This is a placeholder for the generated synthesis."}
                        </p>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-3 gap-4 bg-transparent rounded-sm p-4 border-2 border-black dark:border-white/20">
                        <div className="text-center">
                            <div className="text-black dark:text-[#F3F4F6] text-xs uppercase mb-1 font-bold">Utility</div>
                            <div className="text-2xl font-bold text-black dark:text-[#F3F4F6]">{metrics?.utility || 0}<span className="text-sm font-normal">/10</span></div>
                        </div>
                        <div className="text-center border-l-2 border-black dark:border-white/20">
                            <div className="text-black dark:text-[#F3F4F6] text-xs uppercase mb-1 font-bold">Novelty</div>
                            <div className="text-2xl font-bold text-black dark:text-[#F3F4F6]">{metrics?.novelty || 0}<span className="text-sm font-normal">/10</span></div>
                        </div>
                        <div className="text-center border-l-2 border-black dark:border-white/20">
                            <div className="text-black dark:text-[#F3F4F6] text-xs uppercase mb-1 font-bold">Impact</div>
                            <div className="text-2xl font-bold text-black dark:text-[#F3F4F6]">{metrics?.impact || 0}<span className="text-sm font-normal">/10</span></div>
                        </div>
                    </div>

                    {/* Action items */}
                    <div className="flex gap-3 justify-end pt-4">
                        <button onClick={onClose} className="px-4 py-2 text-sm font-bold text-black dark:text-[#F3F4F6] border border-black dark:border-white/20 bg-transparent hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition-none rounded-sm">
                            Close
                        </button>
                        <button className="px-4 py-2 font-bold text-sm text-white bg-black dark:text-black dark:bg-[#F3F4F6] border border-black dark:border-white/20 hover:bg-transparent hover:text-black dark:hover:bg-transparent dark:hover:text-white transition-none rounded-sm">
                            Save to Notion
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PMBriefModal;
