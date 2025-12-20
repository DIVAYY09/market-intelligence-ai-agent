import React from 'react';

const PMBriefModal = ({ isOpen, onClose, brief, metrics, companyName }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
                onClick={onClose}
            ></div>

            {/* Modal Content */}
            <div className="relative w-full max-w-2xl bg-slate-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden transform transition-all">
                {/* Header */}
                <div className="bg-white/5 px-6 py-4 border-b border-white/5 flex items-center justify-between">
                    <h3 className="text-xl font-semibold text-white tracking-tight">
                        PM Brief: {companyName}
                    </h3>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-white transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Body */}
                <div className="p-6 space-y-6">
                    {/* Brief Text */}
                    <div className="prose prose-invert max-w-none">
                        <h4 className="text-amber-400 text-sm font-bold uppercase tracking-wider mb-2">Executive Summary</h4>
                        <p className="text-gray-300 leading-relaxed text-base">
                            {brief || "No brief available for this signal. This is a placeholder for the generated synthesis."}
                        </p>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-3 gap-4 bg-white/5 rounded-xl p-4 border border-white/5">
                        <div className="text-center">
                            <div className="text-gray-400 text-xs uppercase mb-1">Utility</div>
                            <div className="text-2xl font-bold text-emerald-400">{metrics?.utility || 0}<span className="text-sm text-gray-500">/10</span></div>
                        </div>
                        <div className="text-center border-l border-white/10">
                            <div className="text-gray-400 text-xs uppercase mb-1">Novelty</div>
                            <div className="text-2xl font-bold text-blue-400">{metrics?.novelty || 0}<span className="text-sm text-gray-500">/10</span></div>
                        </div>
                        <div className="text-center border-l border-white/10">
                            <div className="text-gray-400 text-xs uppercase mb-1">Impact</div>
                            <div className="text-2xl font-bold text-purple-400">{metrics?.impact || 0}<span className="text-sm text-gray-500">/10</span></div>
                        </div>
                    </div>

                    {/* Action items */}
                    <div className="flex gap-3 justify-end pt-4">
                        <button onClick={onClose} className="px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors">
                            Close
                        </button>
                        <button className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold text-sm rounded-lg transition-colors shadow-lg shadow-amber-500/20">
                            Save to Notion
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PMBriefModal;
