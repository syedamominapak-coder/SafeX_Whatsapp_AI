"""
AI Fallback Module
Supports OpenRouter (primary) and Gemini (fallback) for AI-powered responses.
"""

from openai import OpenAI
from config.settings import settings


class GeminiFallback:

    def __init__(self):
        self.available = False
        self.openrouter_available = False

        # Try OpenRouter first (uses OpenAI-compatible API)
        if settings.has_openrouter:
            try:
                self.openrouter_client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=settings.OPENROUTER_API_KEY,
                )
                self.openrouter_model = "openai/gpt-4o-mini"
                self.openrouter_available = True
                self.available = True
            except Exception:
                self.openrouter_available = False

        # Fallback to direct Gemini API
        if not self.openrouter_available and settings.has_gemini:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = "gemini-2.0-flash"
                self.available = True
            except Exception:
                self.available = False

    def generate(self, question):
        if not self.available:
            return (
                "I'm sorry, I couldn't find an answer "
                "and the AI assistant is currently unavailable."
            )

        prompt = f"""
You are SafeX AI Business Assistant.

Rules:
1. Answer professionally.
2. Keep answers under 120 words.
3. If the question is about SafeX and you don't know the answer, say:
   "I couldn't find that information in the SafeX knowledge base. Please contact SafeX support."
4. Do not invent company policies or facts.
5. For general knowledge questions, answer accurately and concisely.

User Question:
{question}
"""

        # Try OpenRouter first
        if self.openrouter_available:
            try:
                response = self.openrouter_client.chat.completions.create(
                    model=self.openrouter_model,
                    messages=[
                        {"role": "system", "content": "You are SafeX AI Business Assistant, a helpful customer support AI."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=300,
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                error = str(e)
                # If OpenRouter fails, try Gemini directly
                if hasattr(self, 'gemini_client'):
                    return self._call_gemini(prompt)
                if "429" in error or "quota" in error.lower():
                    return (
                        "🤖 AI assistant is temporarily unavailable because the API "
                        "quota has been reached.\n\n"
                        "Please try again later or ask a SafeX FAQ."
                    )
                return f"AI Error: {error}"

        # Fallback to direct Gemini
        if hasattr(self, 'gemini_client'):
            return self._call_gemini(prompt)

        return "AI assistant is currently unavailable."

    def _call_gemini(self, prompt):
        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            error = str(e)
            if "429" in error or "quota" in error.lower():
                return (
                    "🤖 AI assistant is temporarily unavailable because the Gemini API "
                    "quota has been reached.\n\n"
                    "Please try again later or ask a SafeX FAQ."
                )
            return f"Gemini Error: {error}"