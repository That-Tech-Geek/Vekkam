import React from 'react';
import { HistoryItem } from '../types';

interface HistoryPanelProps {
  history: HistoryItem[];
  onLoadItem: (item: HistoryItem) => void;
  onClear: () => void;
}

const HistoryItemCard: React.FC<{ item: HistoryItem; onLoad: () => void }> = ({ item, onLoad }) => {
    const { apiResponse } = item;
    const isCorrect = apiResponse.prediction === 'Likely Correct';
    const confidencePercentage = Math.round(apiResponse.confidence * 100);

    return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 flex flex-col justify-between space-y-3 transform transition-transform hover:scale-105 hover:border-cyan-500">
            <div>
                <div className="flex justify-between items-start">
                    <p className={`text-lg font-bold ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                        {apiResponse.prediction}
                    </p>
                    <span className="text-sm font-semibold text-cyan-400 bg-slate-700 px-2 py-1 rounded-md">
                        {confidencePercentage}%
                    </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">{item.timestamp}</p>
            </div>
            <button
                onClick={onLoad}
                className="w-full bg-slate-700 hover:bg-cyan-500/20 text-cyan-400 font-semibold py-2 px-3 rounded-md text-sm transition-colors duration-200"
            >
                Load Analysis
            </button>
        </div>
    );
};


export const HistoryPanel: React.FC<HistoryPanelProps> = ({ history, onLoadItem, onClear }) => {
  return (
    <section className="my-16">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-slate-200">Analysis History</h2>
        {history.length > 0 && (
          <button
            onClick={onClear}
            className="bg-red-900/50 hover:bg-red-800/60 text-red-300 font-semibold py-2 px-4 rounded-lg text-sm transition-colors"
          >
            Clear History
          </button>
        )}
      </div>
      {history.length === 0 ? (
        <div className="text-center bg-slate-800/50 border border-slate-700 rounded-xl p-8">
            <p className="text-slate-400">Your past analyses will appear here.</p>
            <p className="text-slate-500 text-sm mt-2">Run an analysis above to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {history.map((item) => (
            <HistoryItemCard key={item.id} item={item} onLoad={() => onLoadItem(item)} />
          ))}
        </div>
      )}
    </section>
  );
};
