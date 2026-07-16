"""
Shared UI helpers for the SafeX AI Support Suite.
Imported by app.py and every page in /pages so the whole app shares one
enterprise-grade design system (sidebar nav, icon set, typography, card styles).
Uses Streamlit's native page routing via st.page_link and st.switch_page.
"""

import streamlit as st
import base64
import os
import pandas as pd
import io
from datetime import datetime


# ---------- Logo ----------
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# ---------- Icon set (lucide-style, stroke-based, no emoji) ----------
def icon(path_d, size=18, stroke_width=2, view_box="0 0 24 24"):
    return (
        f'<svg width="{size}" height="{size}" viewBox="{view_box}" fill="none" '
        f'stroke="currentColor" stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round">{path_d}</svg>'
    )


ICONS = {
    "home": icon('<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>'),
    "chat": icon('<path d="M4 4h16v12H8l-4 4V4Z"/>'),
    "grid": icon('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    "analytics": icon('<path d="M4 20V10"/><path d="M12 20V4"/><path d="M20 20v-7"/><path d="M2 20h20"/>'),
    "users": icon('<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16.5 8.2a3 3 0 1 1 0 5.9"/><path d="M18.8 20a5 5 0 0 0-4-6"/>'),
    "briefcase": icon('<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'),
    "phone": icon('<path d="M6.6 4h3l1.4 5-2.3 1.6a12 12 0 0 0 5.7 5.7l1.6-2.3 5 1.4v3a2 2 0 0 1-2.2 2A18 18 0 0 1 4.6 6.2 2 2 0 0 1 6.6 4Z"/>'),
    "settings": icon('<circle cx="12" cy="12" r="3.2"/><path d="M19.4 13.5a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.9 2.9l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6V20a2 2 0 1 1-4 0v-.2a1.7 1.7 0 0 0-1.1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.9-2.9l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.6-1H4a2 2 0 1 1 0-4h.2a1.7 1.7 0 0 0 1.6-1.1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.9-2.9l.1.1a1.7 1.7 0 0 0 1.9.3H10a1.7 1.7 0 0 0 1-1.6V4a2 2 0 1 1 4 0v.2a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.9 2.9l-.1.1a1.7 1.7 0 0 0-.3 1.9V10a1.7 1.7 0 0 0 1.6 1H20a2 2 0 1 1 0 4h-.2a1.7 1.7 0 0 0-1.6 1Z"/>'),
    "book": icon('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5Z"/><path d="M4 5.5v15A2.5 2.5 0 0 1 6.5 18H20"/>'),
    "globe": icon('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18Z"/>'),
    "sparkles": icon('<path d="M12 3v4M12 17v4M4.2 5.2l2.8 2.8M17 16l2.8 2.8M3 12h4M17 12h4M4.2 18.8 7 16M17 8l2.8-2.8"/>'),
    "message": icon('<path d="M4 4h16v12H8l-4 4V4Z"/>', size=16),
    "layout": icon('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>', size=16),
    "send": icon('<path d="M22 2 11 13"/><path d="m22 2-7 20-4-9-9-4Z"/>', size=16),
    "search": icon('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>', size=16),
    "plus": icon('<path d="M12 5v14M5 12h14"/>', size=16),
    "trend-up": icon('<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>', size=16),
    "trend-down": icon('<path d="M3 7 9 13l4-4 8 8"/><path d="M15 17h6v-6"/>', size=16),
    "check": icon('<path d="M20 6 9 17l-5-5"/>', size=14),
    "clock": icon('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>', size=14),
    "mail": icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>', size=16),
    "tag": icon('<path d="M20.6 12.4 12.9 20a2 2 0 0 1-2.9 0L3 12.9V4h8.9l8.7 8.7a2 2 0 0 1 0 2.9Z"/><circle cx="7.5" cy="8.5" r="1.2"/>', size=16),
    "filter": icon('<path d="M4 5h16M7 12h10M10 19h4"/>', size=16),
    "download": icon('<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M5 21h14"/>', size=16),
    "bot": icon('<rect x="4" y="8" width="16" height="11" rx="2.5"/><path d="M12 8V4"/><circle cx="9" cy="13.5" r="1.2"/><circle cx="15" cy="13.5" r="1.2"/><path d="M2 13h2M20 13h2"/>', size=16),
    "shield": icon('<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6Z"/>', size=16),
    "key": icon('<circle cx="8" cy="15" r="4"/><path d="m10.6 12.4 8.4-8.4M15 8l2 2M18 5l2 2"/>', size=16),
    "bell": icon('<path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10 19a2 2 0 0 0 4 0"/>', size=16),
    "user-circle": icon('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="10" r="3"/><path d="M6.5 19a6 6 0 0 1 11 0"/>', size=16),
    "copy": icon('<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>', size=14),
    "trash": icon('<path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>', size=14),
    "refresh": icon('<path d="M23 4v6h-6M1 20v-6h6M3.5 9a9 9 0 0 1 14.2-3.9L23 10M1 14l5.5 5.2a9 9 0 0 0 13.7-2.3"/>', size=14),
    "external": icon('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>', size=14),
    "info": icon('<circle cx="12" cy="12" r="9"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="12" y1="8" x2="12.01" y2="8"/>', size=14),
}

NAV_ITEMS = [
    ("home", "Home", ICONS["home"], "app.py"),
    ("chat", "Chat", ICONS["chat"], "pages/1_Chat.py"),
    ("dashboard", "Dashboard", ICONS["grid"], "pages/2_Dashboard.py"),
    ("analytics", "Analytics", ICONS["analytics"], "pages/3_Analytics.py"),
    ("leads", "Lead Manager", ICONS["users"], "pages/4_Lead_Manager.py"),
    ("crm", "CRM", ICONS["briefcase"], "pages/5_CRM.py"),
    ("whatsapp", "WhatsApp", ICONS["phone"], "pages/6_WhatsApp.py"),
    ("settings", "Settings", ICONS["settings"], "pages/7_Settings.py"),
]

# Map page keys to their Streamlit page file paths for st.switch_page
PAGE_FILE_MAP = {
    "home": "app.py",
    "chat": "pages/1_Chat.py",
    "dashboard": "pages/2_Dashboard.py",
    "analytics": "pages/3_Analytics.py",
    "leads": "pages/4_Lead_Manager.py",
    "crm": "pages/5_CRM.py",
    "whatsapp": "pages/6_WhatsApp.py",
    "settings": "pages/7_Settings.py",
}


# ---------- Enterprise CSS Design System ----------
def get_enterprise_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }
    #MainMenu, header, footer { visibility: hidden; }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1280px;
    }

    /* ---------- Sidebar (HubSpot-inspired dark nav) ---------- */
    section[data-testid="stSidebar"] {
        background: #0F172A !important;
        border-right: 1px solid rgba(255,255,255,0.06);
        min-width: 240px !important;
        width: 240px !important;
    }
    section[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    div[data-testid="stSidebarNav"] { display: none; }

    /* Style Streamlit page_link to look like our custom nav items */
    div[data-testid="stSidebar"] .st-emotion-cache-1h9usn1 {
        display: none !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.5rem 1rem 1.5rem 1.5rem;
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .nav-section-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #475569;
        padding: 1rem 1.5rem 0.4rem 1.5rem;
    }

    /* Style st.page_link buttons */
    .nav-item-container {
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 0 0.75rem;
    }
    .nav-item-container div[data-testid="stMarkdown"] {
        margin-bottom: 0 !important;
    }
    .nav-item-container button[p=""] {
        all: unset;
    }
    .nav-item-link {
        display: flex !important;
        align-items: center !important;
        gap: 11px !important;
        padding: 0.6rem 0.85rem !important;
        border-radius: 8px !important;
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: all 0.15s ease !important;
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        cursor: pointer !important;
        margin-bottom: 1px !important;
    }
    .nav-item-link:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #E2E8F0 !important;
    }
    .nav-item-link.active {
        background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(79,70,229,0.3) !important;
    }
    .nav-item-link svg { flex-shrink: 0; opacity: 0.8; }
    .nav-item-link.active svg { opacity: 1; }

    /* ---------- Page header (Intercom-style) ---------- */
    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.75rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F1F2F6;
    }
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0;
    }
    .page-title-icon {
        width: 38px; height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: #fff;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .page-subtitle { color: #64748B; font-size: 0.85rem; margin-top: 2px; font-weight: 400; }

    /* ---------- Glassmorphism stat cards ---------- */
    .stat-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        border: 1px solid rgba(226,232,240,0.6);
        padding: 1.25rem;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .stat-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.03);
        transform: translateY(-2px);
        border-color: #CBD5E1;
    }
    .stat-icon {
        width: 42px; height: 42px;
        border-radius: 11px;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .stat-label { font-size: 0.78rem; color: #64748B; font-weight: 500; margin-bottom: 2px; }
    .stat-value { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; }

    /* ---------- Glassmorphism panel (Zendesk-style) ---------- */
    .panel {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        border: 1px solid rgba(226,232,240,0.7);
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease;
    }
    .panel:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .panel-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 1rem;
        display: flex; align-items: center; gap: 8px;
    }

    /* ---------- Pills / Badges ---------- */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 999px;
        white-space: nowrap;
    }
    .pill-green { background: #DCFCE7; color: #166534; }
    .pill-amber { background: #FEF3C7; color: #92400E; }
    .pill-red   { background: #FEE2E2; color: #991B1B; }
    .pill-blue  { background: #DBEAFE; color: #1E40AF; }
    .pill-gray  { background: #F1F5F9; color: #475569; }
    .pill-purple { background: #F3E8FF; color: #6B21A8; }

    hr.divider { border: none; border-top: 1px solid #F1F5F9; margin: 1rem 0; }

    /* ---------- Chat bubbles (Intercom-style) ---------- */
    .msg-row { display: flex; margin-bottom: 12px; animation: fadeIn 0.2s ease; }
    .msg-row.user { justify-content: flex-end; }
    .msg-bubble {
        max-width: 72%;
        padding: 12px 16px;
        border-radius: 14px;
        font-size: 0.9rem;
        line-height: 1.55;
        position: relative;
    }
    .msg-bubble.bot { background: #F1F4F9; color: #0F172A; border-bottom-left-radius: 4px; }
    .msg-bubble.user { background: linear-gradient(135deg, #4F46E5, #6366F1); color: #fff; border-bottom-right-radius: 4px; }
    .msg-meta { font-size: 0.65rem; color: #94A3B8; margin-top: 4px; }
    .msg-meta.user-meta { text-align: right; color: rgba(255,255,255,0.7); }

    .msg-source-badge {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        font-size: 0.65rem;
        font-weight: 600;
        padding: 1px 7px;
        border-radius: 4px;
        margin-top: 5px;
    }
    .msg-source-faq { background: #DBEAFE; color: #1E40AF; }
    .msg-source-gemini { background: #F3E8FF; color: #6B21A8; }
    .msg-source-greeting { background: #DCFCE7; color: #166534; }
    .msg-source-human { background: #FEE2E2; color: #991B1B; }

    /* ---------- Buttons ---------- */
    .btn-primary, .btn-outline, .btn-ghost {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        padding: 0.55rem 1.1rem;
        border-radius: 8px;
        font-size: 0.83rem;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .btn-primary { background: #4F46E5; color: #FFFFFF; border: none; }
    .btn-outline { background: transparent; color: #4F46E5; border: 1.5px solid #C7D2FE; }
    .btn-ghost { background: transparent; color: #64748B; border: none; }

    /* ---------- Row cards ---------- */
    .row-card {
        background: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s ease;
    }
    .row-card:hover { border-color: #CBD5E1; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }

    .avatar {
        width: 34px; height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: #fff;
        display: flex; align-items: center; justify-content: center;
        font-weight: 600; font-size: 0.78rem;
        flex-shrink: 0;
    }

    .score-bar {
        width: 60px;
        height: 4px;
        border-radius: 2px;
        background: #F1F5F9;
        overflow: hidden;
        display: inline-block;
        vertical-align: middle;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.3s ease;
    }

    /* ---------- Animations ---------- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 8px 0;
    }
    .typing-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #94A3B8;
        animation: pulse 1.2s ease-in-out infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    /* ---------- Fix Streamlit widgets spacing ---------- */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div.row-widget.stSelectbox > div {
        border-radius: 8px !important;
    }
    """


# ---------- Page config + global CSS ----------
def setup_page(title, active_nav):
    st.set_page_config(
        page_title=f"SafeX AI Support Suite | {title}",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(f"<style>{get_enterprise_css()}</style>", unsafe_allow_html=True)

    render_sidebar(active_nav)
    render_page_header(title)


def navigate_to(page_key):
    """Use Streamlit's native switch_page for navigation."""
    if page_key in PAGE_FILE_MAP:
        target = PAGE_FILE_MAP[page_key]
        st.switch_page(target)


def render_sidebar(active_nav):
    with st.sidebar:
        # Brand header
        st.markdown(
            """
            <div class="sidebar-brand">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 3v4M12 17v4M4.2 5.2l2.8 2.8M17 16l2.8 2.8M3 12h4M17 12h4M4.2 18.8 7 16M17 8l2.8-2.8"/>
                </svg>
                SafeX AI
            </div>
            <div class="nav-section-label">Platform</div>
            """,
            unsafe_allow_html=True,
        )

        # Render navigation buttons using Streamlit's native page_link
        for key, label, svg, target in NAV_ITEMS:
            active_class = "active" if key == active_nav else ""
            # Use st.button styled as nav items with switch_page
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="secondary" if key != active_nav else "primary",
            ):
                navigate_to(key)

        # Version footer at bottom
        st.markdown(
            "<div style='padding: 1rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 2rem;'>"
            "<div style='font-size:0.7rem; color:#475569;'>v1.0.0 · Enterprise</div>"
            "</div>",
            unsafe_allow_html=True,
        )


PAGE_META = {
    "chat": ("Chat", "sparkles", "AI-powered customer conversations in real time."),
    "dashboard": ("Dashboard", "grid", "Live performance metrics across all support channels."),
    "analytics": ("Analytics", "analytics", "Deep insights into response quality and volume trends."),
    "leads": ("Lead Manager", "users", "Qualified leads captured by the AI assistant."),
    "crm": ("CRM", "briefcase", "HubSpot integration for contact and deal management."),
    "whatsapp": ("WhatsApp", "phone", "WhatsApp Business API automation and broadcast."),
    "settings": ("Settings", "settings", "Configure assistant behavior, integrations, and team."),
}


def render_page_header(title):
    key = None
    for k, v in PAGE_META.items():
        if v[0] == title:
            key = k
            break
    if key is None:
        return
    _, icon_key, subtitle = PAGE_META[key]
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <div class="page-title">
                    <div class="page-title-icon">{ICONS[icon_key]}</div>
                    {title}
                </div>
                <div class="page-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Reusable components ----------
def stat_card(icon_key, bg, fg, label, value, value_color="#0F172A"):
    return f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:{bg}; color:{fg};">{ICONS[icon_key]}</div>
        <div>
            <div class="stat-label">{label}</div>
            <div class="stat-value" style="color:{value_color};">{value}</div>
        </div>
    </div>
    """


def render_metric_row(metrics):
    """Render a row of stat cards from a list of (icon_key, bg, fg, label, value) tuples."""
    cols = st.columns(len(metrics))
    for col, (icon_key, bg, fg, label, value) in zip(cols, metrics):
        with col:
            st.markdown(stat_card(icon_key, bg, fg, label, value), unsafe_allow_html=True)


def source_badge(source):
    """Return HTML for a source badge based on the answer source."""
    if source == "FAQ":
        return '<span class="msg-source-badge msg-source-faq">FAQ</span>'
    elif source in ("Gemini", "AI"):
        return '<span class="msg-source-badge msg-source-gemini">AI</span>'
    elif source == "Greeting":
        return '<span class="msg-source-badge msg-source-greeting">Greeting</span>'
    elif source == "Human":
        return '<span class="msg-source-badge msg-source-human">Human</span>'
    return f'<span class="msg-source-badge msg-source-gemini">{source}</span>'


def confidence_pill(confidence):
    """Return a colored pill for confidence score."""
    if confidence is None:
        return ""
    pct = confidence * 100 if confidence <= 1 else confidence
    if pct >= 80:
        cls = "pill-green"
    elif pct >= 50:
        cls = "pill-amber"
    else:
        cls = "pill-red"
    return f'<span class="pill {cls}">{pct:.0f}%</span>'


def export_csv(data, filename="export.csv"):
    """Convert list of dicts to CSV and return download button HTML."""
    if not data:
        return ""
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_str = csv_buffer.getvalue()
    b64 = base64.b64encode(csv_str.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="btn-outline" style="font-size:0.78rem; padding:0.3rem 0.7rem;">{ICONS["download"]} Export CSV</a>'


def typing_animation():
    """Return HTML for a typing indicator."""
    return """
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """