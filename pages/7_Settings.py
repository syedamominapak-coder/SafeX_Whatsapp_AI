"""
SafeX AI Settings Page
Configure assistant behavior, integrations, team, and security.
Shows real connection status for Gemini, OpenRouter, HubSpot, WhatsApp.
"""

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.utils import setup_page, ICONS
from config.settings import settings
from config.constants import APP_VERSION, APP_NAME, FAQ_SIMILARITY_THRESHOLD, SUPPORTED_LANGUAGES

setup_page("Settings", "settings")

# ---------- Tabs ----------
tab_general, tab_ai, tab_integrations, tab_team, tab_security = st.tabs(
    ["General", "AI Assistant", "Integrations", "Team", "Security"]
)

with tab_general:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["briefcase"]} Workspace</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Workspace name", value="SafeX Support")
        st.selectbox("Timezone", ["Asia/Karachi (PKT)", "UTC", "America/New_York", "Europe/London"])
    with c2:
        st.text_input("Support email", value="support@safex.io")
        st.selectbox("Default language", list(SUPPORTED_LANGUAGES.keys()))

    st.markdown("</div>", unsafe_allow_html=True)

with tab_ai:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["sparkles"]} AI Model Configuration</div>', unsafe_allow_html=True)

    # Real status indicators
    gemini_status = "Connected" if settings.has_gemini else "Not configured"
    gemini_color = "pill-green" if settings.has_gemini else "pill-amber"
    openrouter_status = "Available" if settings.has_openrouter else "Not configured"
    openrouter_color = "pill-green" if settings.has_openrouter else "pill-amber"

    # Show API key status
    gemini_key = settings.GEMINI_API_KEY
    gemini_masked = gemini_key[:6] + "..." if gemini_key else "Not set"

    st.markdown(
        f"""
        <div style="display:flex; gap:1rem; margin-bottom:1.5rem;">
            <div style="flex:1; padding:0.8rem; background:#F8FAFC; border-radius:10px; border:1px solid #F1F5F9;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; font-size:0.85rem; color:#0F172A;">Gemini API</span>
                    <span class="pill {gemini_color}" style="font-size:0.65rem;">{gemini_status}</span>
                </div>
                <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">{gemini_masked}</div>
            </div>
            <div style="flex:1; padding:0.8rem; background:#F8FAFC; border-radius:10px; border:1px solid #F1F5F9;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; font-size:0.85rem; color:#0F172A;">OpenRouter</span>
                    <span class="pill {openrouter_color}" style="font-size:0.65rem;">{openrouter_status}</span>
                </div>
                <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">
                    {'sk-or-...' + settings.OPENROUTER_API_KEY[-4:] if settings.OPENROUTER_API_KEY else 'Not set'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Primary AI Model", ["Gemini 2.0 Flash", "Gemini 2.5 Pro", "GPT-4.1", "Claude Sonnet"])
        st.slider("Response creativity", 0.0, 1.0, 0.3)
    with c2:
        st.selectbox("Fallback behavior", ["Escalate to human agent", "Suggest FAQ articles", "Ask clarifying question"])
        st.slider("Confidence threshold for escalation", 0.0, 1.0, FAQ_SIMILARITY_THRESHOLD)

    st.text_area(
        "System instructions",
        value="Be concise, friendly, and always confirm order numbers before sharing account details.",
        height=90,
    )

    st.toggle("Allow AI to access CRM contact history", value=True)
    st.toggle("Allow AI to issue refunds under a set threshold", value=False)

    st.button("Save assistant settings", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_integrations:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["globe"]} Connected Services</div>', unsafe_allow_html=True)

    # Real integration statuses
    hubspot_status = "Connected" if settings.has_hubspot else "Not connected"
    hubspot_color = "pill-green" if settings.has_hubspot else "pill-gray"
    whatsapp_provider = "Twilio" if settings.has_twilio else "Not connected"
    whatsapp_color = "pill-green" if settings.has_twilio else "pill-gray"

    integrations = [
        ("HubSpot", "CRM sync & contact management", hubspot_status, hubspot_color),
        ("WhatsApp", f"Messaging channel ({whatsapp_provider})", whatsapp_status_text := "Connected" if settings.has_twilio or settings.has_whatsapp else "Not connected",
         whatsapp_color_2 := "pill-green" if settings.has_twilio or settings.has_whatsapp else "pill-gray"),
        ("Gemini", "AI response generation", gemini_status, gemini_color),
        ("OpenRouter", "AI fallback provider", openrouter_status, openrouter_color),
    ]
    # Fix whatsapp entry
    integrations[1] = ("WhatsApp", f"Messaging channel ({whatsapp_provider})",
                       "Connected" if settings.has_twilio or settings.has_whatsapp else "Not connected",
                       "pill-green" if settings.has_twilio or settings.has_whatsapp else "pill-gray")

    for name, desc, status, pill in integrations:
        st.markdown(
            f"""
            <div class="row-card">
                <div>
                    <div style="font-weight:500; color:#0F172A; font-size:0.88rem;">{name}</div>
                    <div style="color:#64748B; font-size:0.78rem;">{desc}</div>
                </div>
                <span class="pill {pill}">{status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_team:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["users"]} Team Members</div>', unsafe_allow_html=True)

    team = [
        ("Ali Hassan", "Owner", "ali.hassan@safex.io"),
        ("Nida Farooq", "Admin", "nida.farooq@safex.io"),
        ("Omar Sheikh", "Agent", "omar.sheikh@safex.io"),
    ]
    for name, role, email in team:
        initials = "".join([p[0] for p in name.split()[:2]]).upper()
        st.markdown(
            f"""
            <div class="row-card">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div class="avatar">{initials}</div>
                    <div>
                        <div style="font-weight:500; color:#0F172A; font-size:0.88rem;">{name}</div>
                        <div style="color:#64748B; font-size:0.78rem;">{email}</div>
                    </div>
                </div>
                <span class="pill pill-blue" style="font-size:0.7rem;">{role}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    with st.form("invite_form"):
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            st.text_input("Email address", placeholder="teammate@company.com", label_visibility="collapsed")
        with c2:
            st.selectbox("Role", ["Agent", "Admin", "Viewer"], label_visibility="collapsed")
        with c3:
            st.form_submit_button("Invite", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with tab_security:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["shield"]} Security & Access Control</div>', unsafe_allow_html=True)

    st.toggle("Require two-factor authentication for all admins", value=True)
    st.toggle("Log all AI-initiated actions for audit review", value=True)
    st.toggle("Mask customer PII in transcripts shown to agents", value=False)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["key"]} API Keys & Tokens</div>', unsafe_allow_html=True)

    # Show real token status
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        gemini_key_display = settings.GEMINI_API_KEY[:10] + "..." if settings.GEMINI_API_KEY else "Not configured"
        st.text_input("Gemini API Key", value=gemini_key_display, type="password", disabled=True)

        hubspot_display = settings.HUBSPOT_ACCESS_TOKEN[:10] + "..." if settings.HUBSPOT_ACCESS_TOKEN else "Not configured"
        st.text_input("HubSpot Access Token", value=hubspot_display, type="password", disabled=True)

    with c_k2:
        twilio_display = settings.TWILIO_ACCOUNT_SID[:8] + "..." if settings.TWILIO_ACCOUNT_SID else "Not configured"
        st.text_input("Twilio Account SID", value=twilio_display, disabled=True)

        st.text_input("Production API Key", value="sx_live_••••••••••••7f2a", type="password")

    st.button("Regenerate Key", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Version info
    st.markdown(
        f"<div style='text-align:center; padding:1rem; color:#94A3B8; font-size:0.75rem;'>"
        f"{APP_NAME} v{APP_VERSION} | Environment: {settings.APP_ENV}</div>",
        unsafe_allow_html=True,
    )