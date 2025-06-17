import json

def load_cards():
    with open("data/cards.json", "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_rewards(card, user_data):
    monthly_spend = int(user_data.get("monthly_spend", 0))
    reward_rate = card["reward_rate"]
    
    if card["reward_type"] == "cashback":
        return int(monthly_spend * reward_rate / 100 * 12)
    elif card["reward_type"] == "points":
        return int(monthly_spend * reward_rate * 0.2 * 12)  # Assuming 1pt = ₹0.2
    else:
        return int(monthly_spend * reward_rate / 200 * 12)

def recommend_cards(user_data):
    cards = load_cards()
    eligible_cards = []

    existing_cards = user_data.get("existing_cards", "").lower().split(",")
    existing_cards = [e.strip() for e in existing_cards if e.strip() and e.lower() != "none"]

    for card in cards:
        if any(name in card["name"].lower() for name in existing_cards):
            continue  # Skip already owned cards

        meets_income = user_data.get("annual_income", 0) >= card["eligibility"]["min_income"]
        matches_category = user_data.get("spending_category", "") in card["categories"]
        matches_benefit = user_data.get("preferred_benefit", "") in [b.lower() for b in card["perks"]]

        if meets_income and (matches_category or matches_benefit):
            card["_matches_category"] = matches_category
            card["_matches_benefit"] = matches_benefit
            eligible_cards.append(card)

    def score_card(card):
        score = 0
        if card["_matches_category"]: score += 20
        if card["_matches_benefit"]: score += 30
        score += card["reward_rate"] * 0.5
        return score

    return sorted(eligible_cards, key=score_card, reverse=True)[:3]
