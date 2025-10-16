export interface StudentData {
  time_of_day: 'morning' | 'afternoon' | 'night';
  stress: number;
  motivation: number;
  option_clicks: number;
  conscientiousness: number;
  difficulty: number;
  recent_practice: number;
  time_on_question: number;
  fatigue_propensity: number;
  study_time_before: number;
  hint_used: boolean;
  baseline_ability: number;
  fatigue_multiplier: number;
}

export interface ActionRecommendation {
  for_student: string;
  for_system: string;
}

export interface ApiResponse {
  prediction: 'Likely Correct' | 'Likely Incorrect';
  confidence: number;
  action_recommendation: ActionRecommendation;
  reasoning: string;
}

export interface HistoryItem {
  id: string;
  timestamp: string;
  studentData: StudentData;
  apiResponse: ApiResponse;
}

export interface StudentProfile {
  name: string;
  description: string;
  data: StudentData;
}
