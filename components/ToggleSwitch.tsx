import React from 'react';

interface ToggleSwitchProps {
  label: string;
  name: string;
  checked: boolean;
  onChange: (name: string, checked: boolean) => void;
}

export const ToggleSwitch: React.FC<ToggleSwitchProps> = ({ label, name, checked, onChange }) => {
  const handleToggle = () => {
    onChange(name, !checked);
  };

  return (
    <div>
      <label className="text-sm font-medium text-slate-300 block mb-2">{label}</label>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={handleToggle}
        className={`${
          checked ? 'bg-cyan-500' : 'bg-slate-700'
        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-800`}
      >
        <span
          aria-hidden="true"
          className={`${
            checked ? 'translate-x-5' : 'translate-x-0'
          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
        />
      </button>
    </div>
  );
};
