
import React from 'react';

interface SegmentedControlProps<T extends string> {
  label: string;
  name: string;
  options: readonly T[];
  value: T;
  onChange: (name: string, value: T) => void;
}

export const SegmentedControl = <T extends string>({
  label,
  name,
  options,
  value,
  onChange,
}: SegmentedControlProps<T>) => {
  return (
    <div>
      <label className="text-sm font-medium text-slate-300 block mb-2">{label}</label>
      <div className="flex w-full bg-slate-800 rounded-lg p-1">
        {options.map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => onChange(name, option)}
            className={`w-full py-2 px-4 rounded-md text-sm font-semibold transition-colors duration-200 capitalize focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-opacity-50 ${
              value === option
                ? 'bg-cyan-500 text-slate-900 shadow-md'
                : 'bg-transparent text-slate-300 hover:bg-slate-700'
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};
