import json
import re
from typing import Dict, Any

def load_cards():
    with open("data/cards.json", "r", encoding="utf-8") as f:
        return json.load(f)

def sanitize_input(text: Any) -> str:
    """Clean user input for consistent matching"""
    if not isinstance(text, str):
        text = str(text)
    return re.sub(r'[^\w\s]', '', text).lower().strip()

def calculate_rewards(card: Dict[str, Any], user_data: Dict[str, Any]) -> int:
    try:
        monthly_spend = int(float(user_data.get("monthly_spend", 0)))
    except (ValueError, TypeError):
        monthly_spend = 0
        
    reward_rate = card.get("reward_rate", 0)
    
    if card.get("reward_type") == "cashback":
        return int(monthly_spend * reward_rate / 100 * 12)
    elif card.get("reward_type") == "points":
        return int(monthly_spend * reward_rate * 0.2 * 12)  # Assuming 1pt = ₹0.2
    else:
        return int(monthly_spend * reward_rate / 200 * 12)

def recommend_cards(user_data: Dict[str, Any]) -> list:
    cards = load_cards()
    eligible_cards = []
    
    # Sanitize all user inputs
    user_data = {k: sanitize_input(v) for k, v in user_data.items()}
    
    # Process existing cards with better mobile handling
    existing_cards = user_data.get("existing_cards", "").split(",")
    existing_cards = [sanitize_input(card) for card in existing_cards 
                   if sanitize_input(card) not in ["", "none", "nil", "na"]]
    
    for card in cards:
        # Skip if user already has this card (fuzzy match)
        card_name_clean = sanitize_input(card["name"])
        if any(ec in card_name_clean for ec in existing_cards):
            continue
            
        # Convert income to int safely
        try:
            user_income = int(float(user_data.get("annual_income", 0)))
            meets_income = user_income >= card["eligibility"]["min_income"]
        except (ValueError, TypeError):
            meets_income = False
            
        # Flexible category matching
        user_category = user_data.get("spending_category", "")
        matches_category = any(
            sanitize_input(user_category) in sanitize_input(cat) 
            for cat in card.get("categories", [])
        )
        
        # Flexible benefit matching
        user_benefit = user_data.get("preferred_benefit", "")
        matches_benefit = any(
            sanitize_input(user_benefit) in sanitize_input(perk)
            for perk in card.get("perks", [])
        )
        
        if meets_income and (matches_category or matches_benefit):
            card["_matches_category"] = matches_category
            card["_matches_benefit"] = matches_benefit
            eligible_cards.append(card)

    def score_card(card: Dict[str, Any]) -> float:
        score = 0
        if card.get("_matches_category", False): 
            score += 20
        if card.get("_matches_benefit", False): 
            score += 30
        score += card.get("reward_rate", 0) * 0.5
        if card.get("annual_fee", 0) == 0:
            score += 10  # Bonus for no annual fee
        return score

    return sorted(eligible_cards, key=score_card, reverse=True)[:3]