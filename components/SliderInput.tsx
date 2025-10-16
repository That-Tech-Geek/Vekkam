
import React from 'react';
import { Tooltip } from './Tooltip';

interface SliderInputProps {
  label: string;
  id: string;
  value: number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  tooltip?: string;
}

export const SliderInput: React.FC<SliderInputProps> = ({
  label,
  id,
  value,
  onChange,
  min = 0,
  max = 1,
  step = 0.01,
  unit = '',
  tooltip,
}) => {
  return (
    <div className="flex flex-col space-y-2">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <label htmlFor={id} className="text-sm font-medium text-slate-300">
            {label}
          </label>
          {tooltip && <Tooltip text={tooltip} />}
        </div>
        <span className="text-sm font-semibold text-cyan-400 bg-slate-700 px-2 py-1 rounded-md">
          {value}{unit}
        </span>
      </div>
      <input
        id={id}
        name={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={onChange}
        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:bg-cyan-400 [&::-webkit-slider-thumb]:rounded-full"
      />
    </div>
  );
};
