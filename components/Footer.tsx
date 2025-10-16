import React from 'react';

export const Footer: React.FC = () => {
    return (
        <footer className="text-center py-10 mt-16 border-t border-slate-800">
            <p className="text-slate-400 max-w-2xl mx-auto font-semibold text-lg">
                <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500">
                    Predict. Adapt. Empower.
                </span>
            </p>
            <p className="mt-4 text-slate-500 text-sm max-w-xl mx-auto">
                The API that helps EdTech apps think like great teachers — predicting student performance, stress, and engagement in real time.
            </p>
        </footer>
    );
};
