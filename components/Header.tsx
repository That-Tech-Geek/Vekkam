import React from 'react';

export const Header: React.FC = () => {
  const handleRequestAccess = () => {
    const tally = (window as any).Tally;
    if (tally) {
      tally.openPopup('3yW0Gx', {
        layout: 'modal',
        width: 700,
        hideTitle: true,
        emoji: {
          text: "👋",
          animation: "wave"
        },
        autoClose: 3000,
      });
    } else {
      console.error('Tally form script not loaded.');
      alert('Could not open the request form. Please try refreshing the page.');
    }
  };

  return (
    <header className="text-center my-12 sm:my-20">
      <h1 className="text-4xl sm:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500 leading-tight">
        AI that feels how students learn.
      </h1>
      <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
        <span className="font-semibold text-slate-300">For EdTech founders and learning platforms</span> who want to drive higher student engagement and outcomes, our product is a plug-and-play intelligence API that translates raw student behavior into adaptive learning decisions.
      </p>
       <p className="mt-4 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
         Unlike generic analytics dashboards or manual personalization tools, we deliver real-time, psychology-informed predictions that help platforms teach every learner like a 1:1 tutor would.
       </p>
       <div className="mt-10">
        <button
          onClick={handleRequestAccess}
          className="bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-bold py-3 px-8 rounded-lg transition-all duration-300 ease-in-out transform hover:scale-105 shadow-lg focus:outline-none focus:ring-4 focus:ring-cyan-500/50"
        >
          Request API Access
        </button>
      </div>
    </header>
  );
};