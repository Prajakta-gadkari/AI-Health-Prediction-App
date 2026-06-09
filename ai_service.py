import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def generate_prediction(
        glucose,
        haemoglobin,
        cholesterol):

    prompt = f"""
You are an expert clinical screening AI assistant. Analyze these patient metrics:
- Glucose: {glucose} mg/dL
- Haemoglobin: {haemoglobin} g/dL
- Cholesterol: {cholesterol} mg/dL

Use these standard clinical reference guidelines for evaluation:
- Normal Glucose: 70 to 140 mg/dL
- Normal Haemoglobin: 12.0 to 17.5 g/dL
- Normal Cholesterol: Below 200 mg/dL

CRITICAL RULE FOR HEALTHY PATIENTS:
If ALL three metrics fall perfectly within the normal guidelines above, you MUST write exactly "• Low Risk" under the Health Risks section. Do not use any other words.

Format your response EXACTLY like this layout:
Health Risks:
• [List prominent risks here, OR write exactly 'Low Risk' if everything is completely normal]

Recommendation:
• [One short, clear actionable advice directive sentence]

Constraints:
- Keep the entire response strictly under 50 words total.
- Do not provide direct medical diagnoses; focus purely on highlighting numerical screening anomalies.
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"AI Prediction Error: {str(e)}"