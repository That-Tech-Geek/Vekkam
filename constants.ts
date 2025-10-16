import { StudentData, StudentProfile } from './types';
import { Type } from '@google/genai';

export const SYSTEM_INSTRUCTION = `You are EduAI — an adaptive learning intelligence layer built for EdTech platforms.

Your job is to analyze a student's real-time behavioral, psychological, and contextual data to predict performance, suggest interventions, and personalize learning flow.

You are powered by data signals like:
- time_of_day
- stress
- motivation
- option_clicks
- conscientiousness
- difficulty
- recent_practice
- time_on_question
- fatigue_propensity
- study_time_before
- hint_used
- baseline_ability
- fatigue_multiplier

These inputs correlate with student accuracy and engagement. Your job is to interpret them and generate *human-like insights and next-step actions* for both:
1. **Students** — personalized feedback and motivation nudges.
2. **Instructors/Apps** — adaptive content difficulty or rest timing.

Always respond in JSON with two keys:
{
  "prediction": "Likely Correct" or "Likely Incorrect",
  "confidence": 0-1,
  "action_recommendation": {
     "for_student": "<short actionable advice>",
     "for_system": "<adjustment the system should make (e.g., increase difficulty, suggest hint, recommend break)>"
  },
  "reasoning": "<short human-readable explanation of your inference>"
}

Be realistic, data-driven, and empathetic — your tone should feel like a coach, not a robot.`;

export const INITIAL_STUDENT_DATA: StudentData = {
  time_of_day: 'night',
  stress: 0.7,
  motivation: 0.8,
  option_clicks: 3,
  conscientiousness: 0.6,
  difficulty: 0.75,
  recent_practice: 0.3,
  time_on_question: 45,
  fatigue_propensity: 0.5,
  study_time_before: 60,
  hint_used: false,
  baseline_ability: 0.65,
  fatigue_multiplier: 0.7
};

export const STUDENT_PROFILES: StudentProfile[] = [
  {
    name: 'Anika',
    description: 'Ambitious achiever, but prone to stress on difficult problems.',
    data: {
      time_of_day: 'afternoon',
      stress: 0.8,
      motivation: 0.9,
      option_clicks: 1,
      conscientiousness: 0.9,
      difficulty: 0.85,
      recent_practice: 0.8,
      time_on_question: 120,
      fatigue_propensity: 0.4,
      study_time_before: 30,
      hint_used: false,
      baseline_ability: 0.8,
      fatigue_multiplier: 0.6,
    },
  },
  {
    name: 'Ben',
    description: 'Hesitant learner who often clicks multiple options, signaling uncertainty.',
    data: {
      time_of_day: 'morning',
      stress: 0.4,
      motivation: 0.6,
      option_clicks: 8,
      conscientiousness: 0.5,
      difficulty: 0.5,
      recent_practice: 0.5,
      time_on_question: 75,
      fatigue_propensity: 0.3,
      study_time_before: 15,
      hint_used: true,
      baseline_ability: 0.55,
      fatigue_multiplier: 0.4,
    },
  },
  {
    name: 'Chloe',
    description: 'Fatigued late-night studier whose performance drops over time.',
    data: {
      time_of_day: 'night',
      stress: 0.6,
      motivation: 0.5,
      option_clicks: 4,
      conscientiousness: 0.7,
      difficulty: 0.6,
      recent_practice: 0.2,
      time_on_question: 60,
      fatigue_propensity: 0.8,
      study_time_before: 120,
      hint_used: false,
      baseline_ability: 0.7,
      fatigue_multiplier: 0.9,
    },
  },
];


export const RESPONSE_SCHEMA = {
    type: Type.OBJECT,
    properties: {
        prediction: { type: Type.STRING, enum: ["Likely Correct", "Likely Incorrect"] },
        confidence: { type: Type.NUMBER },
        action_recommendation: {
            type: Type.OBJECT,
            properties: {
                for_student: { type: Type.STRING },
                for_system: { type: Type.STRING },
            },
            required: ['for_student', 'for_system'],
        },
        reasoning: { type: Type.STRING },
    },
    required: ['prediction', 'confidence', 'action_recommendation', 'reasoning'],
};

export const TOOLTIP_CONTENT = {
  time_of_day: "Reflects when the student is studying. Performance can vary, with late-night sessions often correlating with fatigue.",
  stress: "The student's self-reported or inferred stress level. High stress can impair cognitive function and lead to incorrect answers.",
  motivation: "The student's interest and drive to learn. High motivation is a strong predictor of persistence and success.",
  option_clicks: "The number of times a student changes their answer on a multiple-choice question. High clicks can indicate uncertainty or guessing.",
  conscientiousness: "A personality trait indicating diligence and care. Highly conscientious students are more likely to double-check work.",
  difficulty: "The difficulty level of the current question. A mismatch between difficulty and ability can lead to frustration or boredom.",
  recent_practice: "The student's performance on closely related topics recently. Strong recent performance suggests mastery and preparedness.",
  time_on_question: "How long the student spends on a question. Too little time may suggest guessing; too much may indicate struggle.",
  fatigue_propensity: "A measure of how susceptible the student is to mental fatigue during long study sessions.",
  study_time_before: "The duration of the current study session before this question. Longer sessions can lead to declining performance due to fatigue.",
  hint_used: "Whether the student used a hint on the current question. Hint usage often signals that the student is struggling with the concept.",
  baseline_ability: "The student's overall proficiency in the subject, established from historical performance.",
  fatigue_multiplier: "An algorithmic factor that amplifies the effect of fatigue based on other signals.",
};
