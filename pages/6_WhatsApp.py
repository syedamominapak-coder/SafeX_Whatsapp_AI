"""
SafeX AI WhatsApp Page
WhatsApp Business API management with connection status, automations, templates, and broadcast.
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.utils import setup_page, ICONS, render_metric_row
from services.whatsapp import whatsapp_service
from config.settings import settings

setup_page("WhatsApp", "whatsapp")

# Determine connection status
whatsapp_available = whatsapp_service.available
using_twilio = whatsapp_service.using_twilio
provider_name = "Twilio" if using_twilio else "Meta Cloud API"
connected_number = settings.TWILIO_WHATSAPP_NUMBER if using_twilio else "Not configured"

# ---------- Top Stats ----------
render_metric_row([
    ("phone", "#DCFCE7", "#166534", "Provider", provider_name),
    ("chat", "#EEF2FF", "#4F46E5", "Status", "Connected" if whatsapp_available else "Disconnected"),
    ("users", "#F3E8FF", "#6B21A8", "Broadcast Lists", "6"),
    ("check", "#FEF3C7", "#92400E", "Template Approval", "12 / 14"),
])

st.write("")

# ---------- Connection Status Banner ----------
status_color = "pill-green" if whatsapp_available else "pill-red"
status_text = "Connected" if whatsapp_available else "Not Connected"
status_icon = ICONS["check"] if whatsapp_available else ICONS["info"]

st.markdown(
    f"""
    <div class="panel" style="display:flex; align-items:center; gap:16px; margin-bottom:1rem;">
        <div class="stat-icon" style="background:{'#DCFCE7' if whatsapp_available else '#FEE2E2'};
            color:{'#166534' if whatsapp_available else '#991B1B'}; width:48px; height:48px;">
            {ICONS['phone']}
        </div>
        <div>
            <div style="font-weight:600; font-size:1rem; color:#0F172A;">WhatsApp Business API</div>
            <div style="font-size:0.82rem; color:#64748B;">
                {provider_name} · {connected_number}
            </div>
        </div>
        <span class="pill {status_color}" style="margin-left:auto; font-size:0.75rem;">
            {status_icon} {status_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Tabs ----------
tab_flows, tab_templates, tab_broadcast, tab_settings = st.tabs(
    ["Automated Flows", "Message Templates", "Broadcast", "Connection"]
)

with tab_flows:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["bot"]} Active Automations</div>', unsafe_allow_html=True)

    flows = [
        ("Welcome Message", "Sent when a new contact messages for the first time", True, "pill-green"),
        ("Order Status Lookup", "Detects order number and replies with tracking info", True, "pill-green"),
        ("Business Hours Auto-Reply", "Notifies contacts outside 9am-6pm PKT", True, "pill-green"),
        ("Escalation to Human Agent", "Triggers when the AI confidence score is low", False, "pill-amber"),
    ]
    for name, desc, active, pill in flows:
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(
                f"<div style='font-weight:500; color:#0F172A; font-size:0.88rem;'>{name}</div>"
                f"<div style='color:#64748B; font-size:0.8rem;'>{desc}</div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.toggle(" ", value=active, key=f"flow_{name}", label_visibility="collapsed")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with tab_templates:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["mail"]} Approved Templates</div>', unsafe_allow_html=True)

    templates = [
        ("order_confirmation", "Utility", "Approved"),
        ("shipping_update", "Utility", "Approved"),
        ("abandoned_cart_reminder", "Marketing", "Approved"),
        ("feedback_request", "Marketing", "Pending Review"),
    ]
    for name, category, status in templates:
        pill = "pill-green" if status == "Approved" else "pill-amber"
        st.markdown(
            f"""
            <div class="row-card">
                <div>
                    <div style="font-weight:500; color:#0F172A; font-size:0.85rem;">{name}</div>
                    <div style="color:#64748B; font-size:0.78rem;">{category}</div>
                </div>
                <span class="pill {pill}">{status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_broadcast:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["send"]} New Broadcast</div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        audience = st.selectbox(
            "Audience List",
            ["All customers (3,204)", "Qualified leads (412)", "Cart abandoners (188)", "VIP customers (96)"],
        )
    with col_b2:
        template = st.selectbox(
            "Template",
            ["order_confirmation", "shipping_update", "abandoned_cart_reminder"],
        )

    st.text_area(
        "Preview / Personalization",
        placeholder="Hi {{first_name}}, your order {{order_id}} is on its way!",
        height=100,
    )

    if st.button("Send Broadcast", type="primary", use_container_width=True, disabled=not whatsapp_available):
        st.success("Broadcast queued successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

with tab_settings:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["settings"]} WhatsApp API Configuration</div>', unsafe_allow_html=True)

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        # Show Twilio credentials from .env
        twilio_sid = settings.TWILIO_ACCOUNT_SID or "Not set"
        twilio_sid_masked = twilio_sid[:6] + "..." if twilio_sid != "Not set" else twilio_sid
        st.text_input("Twilio Account SID", value=twilio_sid_masked, disabled=True)

        meta_token = settings.WHATSAPP_TOKEN or "Not set"
        meta_token_masked = meta_token[:6] + "..." if meta_token != "Not set" else meta_token
        st.text_input("Meta Access Token", value=meta_token_masked, type="password", disabled=True)

    with c_s2:
        twilio_number = settings.TWILIO_WHATSAPP_NUMBER or "Not set"
        st.text_input("WhatsApp Number", value=twilio_number, disabled=True)

        meta_phone_id = settings.WHATSAPP_PHONE_NUMBER_ID or "Not set"
        st.text_input("Phone Number ID", value=meta_phone_id, disabled=True)

    st.selectbox("Primary Provider", ["Twilio", "Meta Cloud API", "360dialog", "Gupshup"],
                 index=0 if using_twilio else 1)
    st.toggle("Enable 24-hour session window enforcement", value=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Test message section
    st.markdown(f'<div class="panel-title" style="font-size:0.85rem;">{ICONS["send"]} Send Test Message</div>',
                unsafe_allow_html=True)
    test_number = st.text_input("Test Phone Number", placeholder="+923001234567")
    test_message = st.text_area("Test Message", value="Hello from SafeX AI Assistant!", height=80)

    if st.button("Send Test", type="primary", disabled=not whatsapp_available):
        if test_number:
            with st.spinner("Sending test message..."):
                result = whatsapp_service.send_message(test_number, test_message)
                if result.get("success"):
                    st.success("Test message sent successfully!")
                else:
                    st.error(f"Failed: {result.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a phone number.")

    st.markdown("</div>", unsafe_allow_html=True)