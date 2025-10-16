
import { GoogleGenAI } from "@google/genai";
import { SYSTEM_INSTRUCTION, RESPONSE_SCHEMA } from '../constants';
import { StudentData, ApiResponse } from '../types';

if (!process.env.API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const analyzeStudentPerformance = async (data: StudentData): Promise<ApiResponse> => {
  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: JSON.stringify(data, null, 2),
      config: {
        systemInstruction: SYSTEM_INSTRUCTION,
        responseMimeType: "application/json",
        responseSchema: RESPONSE_SCHEMA,
      },
    });

    const text = response.text.trim();
    const parsedJson = JSON.parse(text);
    return parsedJson as ApiResponse;
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    throw new Error("Failed to get analysis from AI. Please check the console for details.");
  }
};
