import streamlit as st
import base64
import os
from pages.utils import setup_page, ICONS, icon

# Use the shared page setup (adds global CSS and hides Streamlit's
# automatic pages list) and render the sidebar/header.
setup_page("Home", "home")


def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


logo_b64 = get_logo_base64()

# ---------- Page-specific CSS (hero + overview cards) ----------
st.markdown(
    """
    <style>
    .hero-card {
        background: linear-gradient(120deg, #3457D5 0%, #6360E8 48%, #9333EA 100%);
        border-radius: 26px;
        padding: 50px 60px;
        position: relative;
        overflow: hidden;
        color: #FFFFFF;
        margin-bottom: 40px;
        box-shadow: 0 20px 45px -20px rgba(79, 70, 229, 0.55);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-title svg { opacity: 0.85; }
    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 400;
        color: rgba(255,255,255,0.9);
        margin-bottom: 20px;
    }
    .hero-divider {
        width: 44px;
        height: 3px;
        background: rgba(255,255,255,0.55);
        border-radius: 2px;
        margin-bottom: 20px;
    }
    .hero-desc {
        font-size: 0.97rem;
        color: rgba(255,255,255,0.82);
        max-width: 460px;
        line-height: 1.65;
        margin-bottom: 30px;
    }
    .hero-logo-wrap {
        position: absolute;
        right: 64px;
        top: 50%;
        transform: translateY(-50%);
        width: 184px;
        height: 184px;
        background: #FFFFFF;
        border-radius: 50%;
        box-shadow: 0 0 0 16px rgba(255,255,255,0.07);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .hero-logo-wrap img { width: 66%; height: 66%; object-fit: contain; }

    .hero-btn-row { display: flex; gap: 14px; }
    .btn-primary, .btn-outline {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        font-weight: 600;
        padding: 12px 22px;
        border-radius: 10px;
        font-size: 0.93rem;
        cursor: pointer;
        transition: transform 0.12s ease, background 0.15s ease;
        border: none;
    }
    .btn-primary { background: #FFFFFF; color: #4338CA; }
    .btn-primary:hover { background: #F1F1FE; }
    .btn-outline { background: transparent; color: #FFFFFF; border: 1.5px solid rgba(255,255,255,0.55); }
    .btn-outline:hover { background: rgba(255,255,255,0.08); }

    .overview-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.01em;
        margin-bottom: 18px;
    }
    .stat-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #ECEEF3;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 1px 2px rgba(16,24,40,0.04);
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    .stat-card:hover { box-shadow: 0 8px 20px rgba(16,24,40,0.07); transform: translateY(-1px); }
    .stat-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .stat-label { font-size: 0.82rem; color: #6B7280; margin-bottom: 2px; }
    .stat-value { font-size: 1.12rem; font-weight: 700; letter-spacing: -0.01em; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero ----------
logo_html = (
    f"<img src='data:image/png;base64,{logo_b64}' />"
    if logo_b64
    else f"<div style='color:#4338CA;'>{icon('<path d=\"M12 3v4M12 17v4M4.2 5.2l2.8 2.8M17 16l2.8 2.8M3 12h4M17 12h4M4.2 18.8 7 16M17 8l2.8-2.8\"/>', size=56)}</div>"
)

hero_html = f"""
<div class="hero-card">
    <div class="hero-logo-wrap">{logo_html}</div>
    <div class="hero-title">SafeX AI Support Suite {ICONS['sparkles']}</div>
    <div class="hero-subtitle">Enterprise Customer Support Platform</div>
    <div class="hero-divider"></div>
    <div class="hero-desc">
        AI-powered customer support with intelligent FAQ retrieval, lead management,
        CRM integration, WhatsApp automation, multilingual support, and analytics.
    </div>
    <div class="hero-btn-row">
        <a href="/Chat" target="_self" class="btn-primary">{ICONS['message']}Launch Chat</a>
        <a href="/Dashboard" target="_self" class="btn-outline">{ICONS['layout']}View Dashboard</a>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ---------- Platform Overview ----------
st.markdown("<div class='overview-title'>Platform Overview</div>", unsafe_allow_html=True)

stats = [
    (ICONS["book"], "#E7EEFF", "#3457D5", "FAQs", "200+", "#111827"),
    (ICONS["globe"], "#E3F8EC", "#0F9D58", "Languages", "5", "#0F9D58"),
    (ICONS["briefcase"], "#F0EAFE", "#7C3AED", "CRM", "HubSpot", "#7C3AED"),
    (ICONS["sparkles"], "#FEF3DD", "#D97706", "AI Model", "Gemini", "#D97706"),
]

cols = st.columns(4)
for col, (svg, bg, fg, label, value, value_color) in zip(cols, stats):
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon" style="background:{bg}; color:{fg};">{svg}</div>
                <div>
                    <div class="stat-label">{label}</div>
                    <div class="stat-value" style="color:{value_color};">{value}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
