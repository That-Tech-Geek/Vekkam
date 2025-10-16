import React, { useState, useCallback, useEffect } from 'react';
import { INITIAL_STUDENT_DATA, STUDENT_PROFILES } from './constants';
import { StudentData, ApiResponse, HistoryItem } from './types';
import { analyzeStudentPerformance } from './services/geminiService';
import { Header } from './components/Header';
import { SliderInput } from './components/SliderInput';
import { OutputCard } from './components/OutputCard';
import { SegmentedControl } from './components/SegmentedControl';
import { HistoryPanel } from './components/HistoryPanel';
import { Pillars } from './components/Pillars';
import { Footer } from './components/Footer';
import { StudentProfiles } from './components/StudentProfiles';
import { ToggleSwitch } from './components/ToggleSwitch';

const App: React.FC = () => {
  const [studentData, setStudentData] = useState<StudentData>(INITIAL_STUDENT_DATA);
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    try {
      const storedHistory = localStorage.getItem('eduAiHistory');
      if (storedHistory) {
        setHistory(JSON.parse(storedHistory));
      }
    } catch (e) {
      console.error("Failed to parse history from localStorage", e);
      localStorage.removeItem('eduAiHistory');
    }
  }, []);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setStudentData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : Number(value),
    }));
  }, []);

  const handleSegmentChange = useCallback((name: string, value: string) => {
    setStudentData(prev => ({ ...prev, [name]: value }));
  }, []);
  
  const handleBooleanChange = useCallback((name: string, value: boolean) => {
    setStudentData(prev => ({ ...prev, [name]: value }));
  }, []);


  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    setApiResponse(null);
    try {
      const response = await analyzeStudentPerformance(studentData);
      setApiResponse(response);

      const newHistoryItem: HistoryItem = {
        id: new Date().toISOString() + Math.random(),
        timestamp: new Date().toLocaleString(),
        studentData: { ...studentData },
        apiResponse: response,
      };
      const updatedHistory = [newHistoryItem, ...history];
      setHistory(updatedHistory);
      localStorage.setItem('eduAiHistory', JSON.stringify(updatedHistory));

    } catch (err: any) {
      setError(err.message || "An unknown error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadHistoryItem = useCallback((item: HistoryItem) => {
    setStudentData(item.studentData);
    setApiResponse(item.apiResponse);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleClearHistory = useCallback(() => {
    setHistory([]);
    localStorage.removeItem('eduAiHistory');
  }, []);

  const handleLoadProfile = useCallback((data: StudentData) => {
    setStudentData(data);
    setApiResponse(null);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 font-sans p-4 sm:p-8">
      <div className="container mx-auto max-w-7xl">
        <Header />
        
        <main>
            <StudentProfiles profiles={STUDENT_PROFILES} onLoadProfile={handleLoadProfile} />

            {error && (
                <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg relative mb-6" role="alert">
                    <strong className="font-bold">Error: </strong>
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 mt-16">
              {/* Input Panel */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 sm:p-8">
                <h2 className="text-2xl font-bold mb-6 text-slate-200">Live Demo: Student Data Signals</h2>
                <div className="space-y-6">
                  <SegmentedControl
                    label="Time of Day"
                    name="time_of_day"
                    options={['morning', 'afternoon', 'night'] as const}
                    value={studentData.time_of_day}
                    onChange={handleSegmentChange}
                  />
                  <SliderInput label="Stress Level" id="stress" value={studentData.stress} onChange={handleInputChange} />
                  <SliderInput label="Motivation Level" id="motivation" value={studentData.motivation} onChange={handleInputChange} />
                  <SliderInput label="Answer Option Clicks" id="option_clicks" value={studentData.option_clicks} onChange={handleInputChange} min={0} max={10} step={1} />
                  <SliderInput label="Conscientiousness" id="conscientiousness" value={studentData.conscientiousness} onChange={handleInputChange} />
                  <SliderInput label="Question Difficulty" id="difficulty" value={studentData.difficulty} onChange={handleInputChange} />
                  <SliderInput label="Recent Practice Score" id="recent_practice" value={studentData.recent_practice} onChange={handleInputChange} />
                  <SliderInput label="Time on Question (sec)" id="time_on_question" value={studentData.time_on_question} onChange={handleInputChange} min={1} max={300} step={1} unit="s" />
                  <SliderInput label="Fatigue Propensity" id="fatigue_propensity" value={studentData.fatigue_propensity} onChange={handleInputChange} />
                  <SliderInput label="Study Time Before (min)" id="study_time_before" value={studentData.study_time_before} onChange={handleInputChange} min={0} max={180} step={1} unit="m" />
                  <SliderInput label="Baseline Ability" id="baseline_ability" value={studentData.baseline_ability} onChange={handleInputChange} />
                  <SliderInput label="Fatigue Multiplier" id="fatigue_multiplier" value={studentData.fatigue_multiplier} onChange={handleInputChange} />
                  <ToggleSwitch
                      label="Hint Used"
                      name="hint_used"
                      checked={studentData.hint_used}
                      onChange={handleBooleanChange}
                  />

                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading}
                    className="w-full bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                  >
                    {isLoading ? 'Analyzing...' : 'Analyze Performance'}
                  </button>
                </div>
              </div>

              {/* Output Panel */}
              <div>
                <OutputCard data={apiResponse} isLoading={isLoading} />
              </div>
            </div>
            <HistoryPanel history={history} onLoadItem={handleLoadHistoryItem} onClear={handleClearHistory} />
        </main>
        
        <Pillars />
        <Footer />
      </div>
    </div>
  );
};

export default App;
