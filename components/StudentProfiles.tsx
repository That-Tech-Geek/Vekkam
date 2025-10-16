import React from 'react';
import { StudentProfile, StudentData } from '../types';

interface StudentProfilesProps {
  profiles: StudentProfile[];
  onLoadProfile: (data: StudentData) => void;
}

const ProfileCard: React.FC<{ profile: StudentProfile; onLoad: () => void }> = ({ profile, onLoad }) => {
    const icons: { [key: string]: React.ReactNode } = {
        Anika: <span className="text-2xl">👩🏻‍💻</span>,
        Ben: <span className="text-2xl">🤔</span>,
        Chloe: <span className="text-2xl">😴</span>,
    }
    
    return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 text-center flex flex-col items-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-slate-700 flex items-center justify-center">{icons[profile.name] || '🧑‍🎓'}</div>
            <div>
                <h4 className="font-bold text-slate-200">{profile.name}</h4>
                <p className="text-xs text-slate-400 mt-1">{profile.description}</p>
            </div>
            <button 
                onClick={onLoad}
                className="w-full bg-slate-700 hover:bg-cyan-500/20 text-cyan-400 font-semibold py-2 px-3 rounded-md text-sm transition-colors duration-200 mt-auto"
            >
                Load Profile
            </button>
        </div>
    );
};

export const StudentProfiles: React.FC<StudentProfilesProps> = ({ profiles, onLoadProfile }) => {
  return (
    <section className="mb-12">
        <div className="text-center max-w-3xl mx-auto">
             <h2 className="text-3xl font-bold text-slate-200">See How EduAI Adapts</h2>
             <p className="mt-4 text-slate-400">
                We track dozens of metrics in real-time while a student is learning. Our AI interprets these signals to predict performance and adapt the learning experience instantly. 
                Select a mock student profile below to see how it works.
             </p>
        </div>
        <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {profiles.map(profile => (
                <ProfileCard key={profile.name} profile={profile} onLoad={() => onLoadProfile(profile.data)} />
            ))}
        </div>
    </section>
  );
};
