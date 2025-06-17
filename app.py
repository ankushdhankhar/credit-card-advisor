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

# Debugging: Show device info
st.warning(f"Running on: {st.runtime.scriptrunner.get_script_run_context().browser.user_agent}")

# Define question flow
QUESTIONS = [
    ("income", "💰 What's your approximate monthly income? (e.g., 50000)"),
    ("spending_category", "🛒 Primary spending category? (groceries/dining/travel/fuel/online_shopping)"),
    ("monthly_spend", "📊 Monthly spend in this category? (e.g., 10000)"),
    ("credit_score", "🔢 Approximate credit score? (600–900 or 'unknown')"),
    ("existing_cards", "💳 Do you currently use any credit cards? If yes, list them."),
    ("preferred_benefit", "🎯 Preferred benefit? (cashback/lounge_access/air_miles/reward_points)"),
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

# Progress bar
progress = st.session_state.current_q / len(QUESTIONS)
st.progress(progress)

# Chat history
for role, msg in st.session_state.messages:
    with st.chat_message(role, avatar="🧠" if role == "assistant" else "👤"):
        st.write(msg)

# Ask the next question
def ask_question():
    if st.session_state.current_q < len(QUESTIONS):
        key, question = QUESTIONS[st.session_state.current_q]
        st.session_state.messages.append(("assistant", question))
        return key
    return None

# Show a single recommendation card
def show_recommendation(card, user_data):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            if card.get("image_url"):
                st.image(card["image_url"], width=100)
            else:
                st.markdown("🖼️ Image not available")
        with col2:
            st.subheader(card["name"])
            st.caption(f"**Issuer:** {card['issuer']} | **Annual Fee:** ₹{card['annual_fee']}")
            annual_rewards = calculate_rewards(card, user_data)
            st.success(f"**You could earn ₹{annual_rewards}/year in {card['reward_type']}**")

            with st.expander("Why this card?"):
                with st.spinner("Generating reason..."):
                    reason = groq.generate_recommendation_reason(card, user_data)
                    st.write(reason)

            apply_link = card.get("apply_link", "#")
            st.link_button("Apply Now", apply_link, use_container_width=True, disabled=(apply_link == "#"))

# Show table comparison
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

# Auto-ask question on load
if st.session_state.current_q < len(QUESTIONS) and (
    not st.session_state.messages or st.session_state.messages[-1][0] == "user"
):
    ask_question()
    st.rerun()

# Chat input handling
if prompt := st.chat_input("Your answer..."):
    st.session_state.messages.append(("user", prompt))
    current_key = QUESTIONS[st.session_state.current_q][0]
    st.session_state.user_data[current_key] = prompt

    # Validate income & spend
    if current_key == "income" or current_key == "monthly_spend":
        try:
            value = int(prompt)
            if value < 0:
                raise ValueError
            if current_key == "income":
                st.session_state.user_data["annual_income"] = value * 12
        except ValueError:
            st.error("Please enter a valid positive number.")
            st.stop()
    elif current_key == "credit_score":
        if prompt.lower() != "unknown":
            try:
                score = int(prompt)
                if score < 300 or score > 900:
                    raise ValueError
            except ValueError:
                st.error("Credit score must be between 300–900 or 'unknown'.")
                st.stop()

    # Go to next question
    st.session_state.current_q += 1

    if st.session_state.current_q < len(QUESTIONS):
        ask_question()
        st.rerun()
    else:
        with st.spinner("Finding the best cards for you..."):
            try:
                recommendations = recommend_cards(st.session_state.user_data)
                st.session_state.recommended_cards = recommendations
                st.toast("✅ Cards successfully recommended", icon="✅")
            except Exception as e:
                st.error(f"❌ Error recommending cards: {e}")
                st.stop()
        st.rerun()

# Show recommendations
if st.session_state.current_q >= len(QUESTIONS) and st.session_state.recommended_cards:
    st.markdown("## 🧾 Your Profile Summary")
    with st.expander("Click to view", expanded=False):
        for k, v in st.session_state.user_data.items():
            st.write(f"**{k.replace('_', ' ').title()}**: {v}")
    st.divider()

    st.markdown(f"## 💳 Here are your top {len(st.session_state.recommended_cards)} recommendations")
    for card in st.session_state.recommended_cards:
        show_recommendation(card, st.session_state.user_data)
        st.divider()

    show_comparison(st.session_state.recommended_cards, st.session_state.user_data)

# Restart app
if st.button("🔄 Restart Conversation"):
    st.session_state.messages = []
    st.session_state.user_data = {}
    st.session_state.current_q = 0
    st.session_state.recommended_cards = []
    st.rerun()
