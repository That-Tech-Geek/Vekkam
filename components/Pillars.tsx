import React from 'react';

const PillarCard: React.FC<{ icon: React.ReactNode; title: string; hook: string; children: React.ReactNode }> = ({ icon, title, hook, children }) => (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 h-full flex flex-col">
        <div className="flex items-center mb-4">
            <div className="text-cyan-400 mr-4">{icon}</div>
            <h3 className="text-xl font-bold text-slate-200">{title}</h3>
        </div>
        <p className="text-slate-400 flex-grow">{children}</p>
        <p className="mt-4 text-cyan-300 italic text-sm font-medium">"{hook}"</p>
    </div>
);

const TargetIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>;
const ChartIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>;
const PlugIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9 17v2a3 3 0 006 0v-2M9 7V5a3 3 0 016 0v2m-6 2h6" /></svg>;
const HeartIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>;


export const Pillars: React.FC = () => {
    return (
        <section className="my-16 sm:my-24">
            <h2 className="text-3xl font-bold text-slate-200 text-center mb-10">The Intelligence Layer for Modern Learning</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <PillarCard icon={<TargetIcon />} title="Adaptive Precision" hook="Every student gets a uniquely intelligent learning curve.">
                    Uses behavioral + cognitive signals to dynamically adjust learning paths.
                </PillarCard>
                <PillarCard icon={<ChartIcon />} title="Predictive Clarity" hook="Know before they fail.">
                    Transforms messy engagement data into actionable performance probabilities.
                </PillarCard>
                <PillarCard icon={<PlugIcon />} title="Effortless Integration" hook="Add a brain, not another system.">
                    Works as a lightweight API that plugs into any LMS, app, or EdTech backend.
                </PillarCard>
                <PillarCard icon={<HeartIcon />} title="Human-Centric AI" hook="Empathy engineered into every prediction.">
                    Rooted in psychology and pedagogy, not black-box ML.
                </PillarCard>
            </div>
        </section>
    );
};
