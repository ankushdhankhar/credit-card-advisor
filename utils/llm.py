import os
from groq import Groq
from typing import Dict, Any

class GroqClient:
    def __init__(self, model: str = "llama3-70b-8192"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model

    def generate_recommendation_reason(self, card: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        try:
            monthly_income = int(user_data.get("annual_income", 0)) // 12
        except (ValueError, TypeError):
            monthly_income = 0

        monthly_spend = user_data.get("monthly_spend", "unknown")
        category = user_data.get("spending_category", "various categories")
        benefit = user_data.get("preferred_benefit", "multiple benefits")

        prompt = f"""Generate a short 2-sentence personalized explanation for why this card is recommended:

User Profile:
- Monthly Income: ₹{monthly_income}
- Spends ₹{monthly_spend}/month on {category}
- Prefers: {benefit}

Card Features:
- Name: {card['name']}
- Rewards: {card['reward_rate']}% {card['reward_type']}
- Key Perks: {', '.join(card['perks'][:2])}

Focus on how it matches their spending and preferences."""
        
        return self.get_response(prompt)

    def get_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.4,
                
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API error: {e}")
            return "This card closely aligns with your spending habits and preferred benefits."
