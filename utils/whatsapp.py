import streamlit as st
import os 
from twilio.rest import Client
from typing import List, Dict

try:
    import streamlit as st
    TWILIO_SID = st.secrets["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH = st.secrets["TWILIO_AUTH_TOKEN"]
    WHATSAPP_NUMBER = st.secrets["TWILIO_WHATSAPP_NUMBER"]
except Exception:
    # Fallback to .env for local development
    from dotenv import load_dotenv
    load_dotenv()
    TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
    WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

def send_whatsapp_message(to_number: str, recommended_cards: List[Dict]) -> str:
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)

        message_body = "*Your Top Credit Card Recommendations:*\n\n"
        for card in recommended_cards:
            message_body += f"- {card['name']} ({card['reward_rate']}% {card['reward_type'].capitalize()})\n"

        message = client.messages.create(
            body=message_body,
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{to_number}"
        )
        return f"✅ Message sent successfully to {to_number}"
    except Exception as e:
        return f"❌ Failed to send: {str(e)}"
