# 🛡️ SafeX AI Support Suite

**Enterprise-Grade AI-Powered Customer Support Platform**

SafeX AI is a full-featured, multi-channel customer support platform that combines intelligent FAQ retrieval, Google Gemini AI conversations, lead management, CRM integration (HubSpot), WhatsApp automation, multilingual support, and real-time analytics — all in a polished, single-page web application built with Streamlit.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Chat** | Real-time conversational interface with typing indicators, source badges (FAQ / AI / Human), and message history |
| 📚 **FAQ Engine** | 200+ pre-loaded Q&A pairs with semantic similarity matching for instant, accurate answers |
| 🧠 **Gemini AI Fallback** | Google Gemini generates intelligent responses when no FAQ match is found |
| 🌍 **Multilingual** | Supports English, Urdu, Arabic, French, and Spanish with automatic translation |
| 👤 **Lead Collection** | Automatically captures qualified leads when users inquire about pricing, demos, or subscriptions |
| 📊 **Analytics Dashboard** | Response times, conversation volume, FAQ hit rates, lead conversion metrics, and trend analysis |
| 💼 **CRM Integration** | HubSpot integration for seamless contact and deal management |
| 📱 **WhatsApp Automation** | WhatsApp Business API integration for automated messaging and broadcasts |
| 👨‍💼 **Human Handover** | Escalates conversations to real support agents when requested |
| 🎨 **Enterprise UI** | Dark sidebar navigation, glassmorphism cards, Inter font, lucide-style SVG icons |

---

## 🏗️ Architecture

```
User Message
    │
    ▼
Intent Detection
    ├── Greeting → Welcome message
    ├── Goodbye → Farewell message
    ├── Human Handover → Escalate to agent
    └── Support Question
            │
            ▼
    FAQ Engine (Cosine Similarity ≥ 60%)
        ├── Match Found → Return FAQ answer
        └── No Match → Google Gemini generates response
```

The system uses a **cascading fallback architecture** — it tries the fastest/cheapest option first and escalates to AI only when necessary.

---

## 📁 Project Structure

```
SafeX-AI-Assistant/
│
├── app.py                          # Homepage / entry point
├── pages/                          # Streamlit multi-page UI
│   ├── utils.py                    # Shared design system (CSS, icons, nav)
│   ├── 1_Chat.py                   # AI Chat interface
│   ├── 2_Dashboard.py              # Live performance metrics
│   ├── 3_Analytics.py              # Deep analytics
│   ├── 4_Lead_Manager.py           # Lead management
│   ├── 5_CRM.py                    # HubSpot CRM integration
│   ├── 6_WhatsApp.py               # WhatsApp automation
│   └── 7_Settings.py               # Configuration panel
│
├── chatbot/                        # Core AI engine
│   ├── router.py                   # Message routing logic
│   ├── intent.py                   # Intent detection
│   ├── faq_engine.py               # FAQ similarity search
│   ├── similarity.py               # Cosine similarity matching
│   ├── openai_fallback.py          # Google Gemini fallback
│   ├── handover.py                 # Human agent escalation
│   ├── lead_collection.py          # Lead capture
│   ├── preprocessing.py            # Text normalization
│   └── translator.py               # Multilingual translation
│
├── config/                         # Configuration
│   ├── constants.py                # Thresholds, keywords, paths
│   └── settings.py                 # API keys, environment vars
│
├── database/                       # Data persistence
│   ├── db.py                       # SQLite connection
│   ├── models.py                   # Table schemas
│   └── queries.py                  # SQL query helpers
│
├── services/                       # External integrations
│   ├── whatsapp.py                 # WhatsApp Business API
│   ├── crm.py                      # HubSpot CRM
│   ├── analytics.py                # Analytics computation
│   └── language.py                 # Language detection
│
├── dashboard/                      # Dashboard logic
│   └── analytics.py
│
├── data/                           # Persistent storage
│   ├── SafeX_200_FAQ_Dataset_new.xlsx  # FAQ knowledge base
│   └── safex_assistant.db              # SQLite database
│
├── webhook_server.py               # Webhook handler
├── assets/                         # Static files
│   ├── logo.png
│   └── style.css
│
├── requirements.txt                # Python dependencies
└── .env                            # Environment variables
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Python) with custom enterprise CSS |
| **AI / NLP** | Google Gemini API, cosine similarity (sentence embeddings) |
| **Database** | SQLite |
| **CRM** | HubSpot API |
| **Messaging** | WhatsApp Business API |
| **Languages** | Python 3, pandas, numpy, scikit-learn |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/syedamominapak-coder/SafeX_Whatsapp_AI.git
cd SafeX_Whatsapp_AI

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (Gemini, HubSpot, WhatsApp)
```

### Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔧 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key

# HubSpot CRM
HUBSPOT_API_KEY=your_hubspot_api_key

# WhatsApp Business API
WHATSAPP_API_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
```

---

## 📊 Pages Overview

| Page | Route | Purpose |
|------|-------|---------|
| **Home** | `/` | Platform overview with quick stats |
| **Chat** | `/Chat` | AI-powered customer conversations |
| **Dashboard** | `/Dashboard` | Live performance metrics |
| **Analytics** | `/Analytics` | Deep insights and trends |
| **Lead Manager** | `/Lead_Manager` | Qualified leads from conversations |
| **CRM** | `/CRM` | HubSpot contact and deal management |
| **WhatsApp** | `/WhatsApp` | WhatsApp automation and broadcasts |
| **Settings** | `/Settings` | Assistant behavior and integrations |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Syeda Mominapak**  
[GitHub](https://github.com/syedamominapak-coder)

---

<p align="center">
  Built with ❤️ using Streamlit & Google Gemini
</p>