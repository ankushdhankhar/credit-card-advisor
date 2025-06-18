# 💳 Credit Card Advisor App

An AI-powered credit card advisor app built using **Streamlit**, **Groq API (LLaMA-3)**, and **Twilio WhatsApp API**, designed to help users find the most suitable credit cards based on their spending patterns and preferences.

---

## 🚀 Features

- 🔍 **Personalized Recommendations** based on user inputs  
- 📊 **Reward Simulation** using monthly spending data  
- 📈 **Card Comparison** with annual cashback/points estimates  
- 🤖 **LLM-powered Reasoning** ("Why this card?") via **Groq API**  
- 📱 **WhatsApp Integration** to deliver results using **Twilio API**  
- ☁️ **Hosted on Streamlit Cloud** for easy access anywhere  

---

## 🛠️ Tech Stack

| Component     | Technology                     |
|---------------|--------------------------------|
| UI/Frontend   | Streamlit                      |
| AI/LLM        | Groq (LLaMA-3)                 |
| Messaging     | Twilio WhatsApp API            |
| Backend Logic | Python                         |
| Hosting       | Streamlit Cloud                |


---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ankushdhankhar/credit-card-advisor.git
cd credit-card-advisor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your secrets

Use `st.secrets` if deploying on Streamlit Cloud, or create a `.env` file for local development:

```
# .streamlit/secrets.toml (for Streamlit Cloud)

GROQ_API_KEY = "your_groq_api_key"
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
```

### 4. Run the App

```
streamlit run app.py

```

### It will run on : http://localhost:8501
---


## 💬 WhatsApp Integration (Twilio Sandbox)

To enable WhatsApp messaging, follow these steps:

### ✅ Setup Steps:

1. **Sign up** at [Twilio](https://www.twilio.com/)
2. **Activate** the WhatsApp Sandbox in your Twilio Console
3. **Join the sandbox** by sending the join code (e.g., `join nation-lion`) to:
   `+1 415 523 8886` via WhatsApp
4. In your code, use the following sandbox number:
   `whatsapp:+14155238886`

> ⚠️ **Note:** Only verified numbers (those who have joined the sandbox) can receive messages unless you're using a paid Twilio account.

---

## 🧠 How It Works

1. **User Input**
   Users provide their:

   * Monthly Salary
   * Monthly Spending
   * Preferred Benefit (e.g., cashback, rewards)
   * And more...

2. **Filtering & Scoring**
   A custom engine filters and ranks credit cards based on:

   * Relevant spending categories (e.g., dining, travel, groceries)
   * Reward type match with user preference

3. **LLM Reasoning**
   A large language model via **Groq API** generates natural-language justifications for each recommendation.

4. **Reward Simulation**
   Calculates expected **annual cashback or reward points** based on spending and card-specific rates.

5. **WhatsApp Delivery**
   Sends the top credit card recommendations directly to the user's WhatsApp using **Twilio API**.

---

## 🎯 How to try the App

1. Launch the app (or visit https://credit-card-advisor.streamlit.app/ ) and **fill in all requested inputs**
2. After answering the **Preferred Benefit** question:

   * The app will display the **top 3 recommended credit cards**
   * A **comparison table** and **user profile summary** will be shown
3. To receive recommendations via WhatsApp:

   * **Send `join nation-lion` to `+1 415 523 8886`** via WhatsApp to join the Twilio Sandbox
   * Click on "Send to WhatsApp" within the app

---

## 📹 Demo Videos

Watch the app in action! Click the link below to view demo videos hosted on Google Drive:

- 🔍 [Running app on different Devices](https://drive.google.com/drive/folders/12S003TvSttyjxK1UbDQEWbWvAKQA9Xto?usp=sharing)

---

## 🤝 Connect

📧 [ankushdhankhar3002@gmail.com](mailto:ankushdhankhar3002@gmail.com)  
💼 [LinkedIn](https://in.linkedin.com/in/ankush-dhankhar-616a48250)

