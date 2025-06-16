import streamlit as st
from utils.llm import GroqClient
from utils.recommender import recommend_cards, calculate_rewards
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize LLM
groq = GroqClient()

# Define question flow
QUESTIONS = [
    ("income", "What's your approximate monthly income? (e.g., 50000)"),
    ("spending_category", "Primary spending category? (groceries/dining/travel/fuel/online_shopping)"),
    ("monthly_spend", "How much do you spend monthly in this category? (e.g., 10000)"),
    ("credit_score", "Approximate credit score? (600-900 or 'unknown')"),
    ("preferred_benefit", "Preferred benefit? (cashback/lounge_access/air_miles/reward_points)"),
]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "recommended_cards" not in st.session_state:
    st.session_state.recommended_cards = []

# Title
st.title("💳 Smart Credit Card Advisor")

# Show message history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# Ask the next question
def ask_question():
    if st.session_state.current_q < len(QUESTIONS):
        key, question = QUESTIONS[st.session_state.current_q]
        st.session_state.messages.append(("assistant", question))
        return key
    return None

# Display a single card recommendation
def show_recommendation(card, user_data):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if card.get("image_url"):
                st.image(card["image_url"], width=150)
            else:
                st.markdown("🖼️ Image not available")
        
        with col2:
            st.subheader(card["name"])
            st.caption(f"**Issuer:** {card['issuer']} | **Annual Fee:** ₹{card['annual_fee']}")
            
            annual_rewards = calculate_rewards(card, user_data)
            st.success(f"**You could earn ₹{annual_rewards}/year in {card['reward_type']}**")
            
            with st.expander("Why this card?"):
                reason = groq.generate_recommendation_reason(card, user_data)
                st.write(reason)
            
            st.link_button("Apply Now", "#", use_container_width=True)

# Show card comparison table
def show_comparison(cards, user_data):
    st.markdown("## 📊 Compare Recommended Cards")
    
    data = []
    for card in cards:
        data.append({
            "Card Name": card["name"],
            "Issuer": card["issuer"],
            "Annual Fee (₹)": card["annual_fee"],
            "Reward Type": card["reward_type"],
            "Reward Rate": f"{card['reward_rate']}%",
            "Est. Annual Rewards (₹)": calculate_rewards(card, user_data),
            "Top Perks": ", ".join(card["perks"][:2]),
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Show first question if app just started
if not st.session_state.messages and st.session_state.current_q == 0:
    ask_question()
    st.rerun()

# Input handler
if prompt := st.chat_input("Your answer..."):
    st.session_state.messages.append(("user", prompt))
    
    current_key = QUESTIONS[st.session_state.current_q][0]
    st.session_state.user_data[current_key] = prompt
    
    # Convert income to annual income
    if current_key == "income":
        try:
            st.session_state.user_data["annual_income"] = int(prompt) * 12
        except ValueError:
            st.error("Please enter a valid number")
            st.stop()
    
    # Move to next question
    st.session_state.current_q += 1
    
    if st.session_state.current_q < len(QUESTIONS):
        ask_question()
        st.rerun()
    else:
        # Final step – store results (but don't rerun now)
        recommendations = recommend_cards(st.session_state.user_data)
        st.session_state.recommended_cards = recommendations
        
        st.session_state.messages.append((
            "assistant",
            f"Here are your top {len(recommendations)} recommendations:"
        ))

# Show recommendations if already available
if st.session_state.current_q >= len(QUESTIONS) and st.session_state.recommended_cards:
    for card in st.session_state.recommended_cards:
        show_recommendation(card, st.session_state.user_data)
    
    show_comparison(st.session_state.recommended_cards, st.session_state.user_data)

# Restart conversation
if st.button("🔄 Restart Conversation"):
    st.session_state.messages = []
    st.session_state.user_data = {}
    st.session_state.current_q = 0
    st.session_state.recommended_cards = []
    st.rerun()
