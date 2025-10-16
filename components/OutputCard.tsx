
import React from 'react';
import { ApiResponse } from '../types';

interface OutputCardProps {
  data: ApiResponse | null;
  isLoading: boolean;
}

const InfoBlock: React.FC<{ icon: React.ReactNode; title: string; children: React.ReactNode }> = ({ icon, title, children }) => (
    <div className="bg-slate-800 p-4 rounded-lg">
        <div className="flex items-center mb-2">
            <div className="text-cyan-400 mr-3">{icon}</div>
            <h3 className="font-semibold text-slate-300">{title}</h3>
        </div>
        <p className="text-slate-400 text-sm">{children}</p>
    </div>
);

const UserIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
);

const SystemIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
    </svg>
);

const BrainIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547a2 2 0 00-.547 1.806l.477 2.387a6 6 0 00.517 3.86l.158.318a6 6 0 00.517 3.86l2.387.477a2 2 0 001.806-.547a2 2 0 00.547-1.806l-.477-2.387a6 6 0 00-.517-3.86l-.158-.318a6 6 0 00-.517-3.86l-2.387-.477zM12 8a2 2 0 100-4 2 2 0 000 4z" />
    </svg>
);

export const OutputCard: React.FC<OutputCardProps> = ({ data, isLoading }) => {
    const renderContent = () => {
        if (isLoading) {
            return (
                <div className="flex flex-col items-center justify-center h-full space-y-4">
                     <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-cyan-400"></div>
                     <p className="text-slate-400">EduAI is thinking...</p>
                </div>
            );
        }

        if (!data) {
            return (
                <div className="flex flex-col items-center justify-center h-full text-center">
                    <BrainIcon />
                    <h3 className="mt-4 text-xl font-semibold text-slate-300">Awaiting Analysis</h3>
                    <p className="mt-2 text-slate-500">Adjust the student data on the left and click "Analyze Performance" to see EduAI's insights.</p>
                </div>
            );
        }

        const isCorrect = data.prediction === 'Likely Correct';
        const confidencePercentage = Math.round(data.confidence * 100);

        return (
            <div className="flex flex-col space-y-6">
                <div className="text-center">
                    <p className="text-sm text-slate-400">Prediction</p>
                    <p className={`text-3xl font-bold ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                        {data.prediction}
                    </p>
                </div>

                <div>
                    <div className="flex justify-between mb-1">
                        <span className="text-base font-medium text-slate-300">Confidence</span>
                        <span className="text-sm font-medium text-cyan-400">{confidencePercentage}%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2.5">
                        <div className="bg-cyan-500 h-2.5 rounded-full" style={{ width: `${confidencePercentage}%` }}></div>
                    </div>
                </div>

                <div className="space-y-4">
                     <h3 className="text-lg font-semibold text-slate-200 border-b border-slate-700 pb-2">Action Recommendations</h3>
                     <InfoBlock icon={<UserIcon />} title="For the Student">
                        {data.action_recommendation.for_student}
                     </InfoBlock>
                     <InfoBlock icon={<SystemIcon />} title="For the System">
                        {data.action_recommendation.for_system}
                     </InfoBlock>
                </div>
                 <div>
                    <h3 className="text-lg font-semibold text-slate-200 border-b border-slate-700 pb-2 mb-2">Reasoning</h3>
                    <p className="text-slate-400 text-sm italic">"{data.reasoning}"</p>
                </div>

            </div>
        );
    };

    return (
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 sm:p-8 h-full min-h-[600px] sticky top-10">
            {renderContent()}
        </div>
    );
};
