from groq import Groq
import os

class GroqClient:
    def __init__(self, model="llama3-70b-8192"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
    
    def generate_recommendation_reason(self, card, user_data):
        prompt = f"""Generate a 2-sentence personalized explanation for why this card is recommended:
        
        User Profile:
        - Monthly Income: ₹{user_data.get('annual_income', 0)//12}
        - Spends ₹{user_data.get('monthly_spend', 0)}/month on {user_data.get('spending_category', '')}
        - Prefers: {user_data.get('preferred_benefit', '')}
        
        Card Features:
        - Name: {card['name']}
        - Rewards: {card['reward_rate']}% {card['reward_type']}
        - Key Perks: {', '.join(card['perks'][:2])}
        
        Focus on how it matches their spending habits and preferred benefits."""
        
        return self.get_response(prompt)
    
    def get_response(self, prompt):
     try:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
     except Exception as e:
        print(f"Groq API error: {e}")  # 👈 Add this line
        return "This card matches your spending habits and preferred benefits."
