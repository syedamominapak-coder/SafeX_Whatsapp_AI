"""
SafeX AI CRM Page
HubSpot integration management with connection status, sync history, field mapping.
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.utils import setup_page, ICONS, render_metric_row
from services.crm import crm_service
from config.settings import settings

setup_page("CRM", "crm")

# Check HubSpot connection
hubspot_available = crm_service.available

# ---------- Connection Status ----------
col_status, col_action = st.columns([3, 1])

with col_status:
    status_color = "pill-green" if hubspot_available else "pill-red"
    status_text = "Connected" if hubspot_available else "Not Connected"
    status_icon = ICONS["check"] if hubspot_available else ICONS["info"]

    st.markdown(
        f"""
        <div class="panel" style="display:flex; align-items:center; gap:16px;">
            <div class="stat-icon" style="background:{'#DCFCE7' if hubspot_available else '#FEE2E2'};
                color:{'#166534' if hubspot_available else '#991B1B'}; width:48px; height:48px;">
                {ICONS['briefcase']}
            </div>
            <div>
                <div style="font-weight:600; font-size:1rem; color:#0F172A;">HubSpot CRM</div>
                <div style="font-size:0.82rem; color:#64748B;">
                    {settings.HUBSPOT_ACCESS_TOKEN[:8] + '...' if hubspot_available else 'No API token configured'}
                </div>
            </div>
            <span class="pill {status_color}" style="margin-left:auto; font-size:0.75rem;">
                {status_icon} {status_text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_action:
    st.write("")
    if st.button("Test Connection", use_container_width=True, type="primary", disabled=not hubspot_available):
        with st.spinner("Testing HubSpot connection..."):
            result = crm_service.get_contacts(limit=1)
            if result.get("success"):
                st.success("Connection verified!")
            else:
                st.error(f"Connection failed: {result.get('error', 'Unknown error')}")

st.write("")

# ---------- Metrics ----------
if hubspot_available:
    contacts_result = crm_service.get_contacts(limit=100)
    contact_count = len(contacts_result.get("contacts", [])) if contacts_result.get("success") else 0
else:
    contact_count = 0

render_metric_row([
    ("users", "#EEF2FF", "#4F46E5", "Contacts Synced", f"{contact_count:,}" if contact_count else "0"),
    ("briefcase", "#DCFCE7", "#166534", "Open Deals", "0"),
    ("tag", "#FEF3C7", "#92400E", "Pipelines", "1"),
    ("clock", "#F3E8FF", "#6B21A8", "Sync Interval", "Manual"),
])

st.write("")

# ---------- Sync Section ----------
col_left, col_right = st.columns([1.4, 1])

with col_left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["refresh"]} Sync History</div>', unsafe_allow_html=True)

    # Show recent syncs from database leads
    from database.queries import get_all_leads
    leads = get_all_leads()
    synced_leads = [l for l in leads if l.crm_synced == "Yes"]

    if synced_leads:
        for lead in synced_leads[-5:]:
            st.markdown(
                f"""
                <div style="padding:0.6rem 0; border-bottom:1px solid #F1F5F9;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-weight:500; font-size:0.85rem; color:#0F172A;">{lead.name}</span>
                        <span class="pill pill-green" style="font-size:0.6rem;">Synced</span>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B;">
                        {lead.email} · {lead.created_at.strftime('%Y-%m-%d %H:%M') if lead.created_at else 'N/A'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div style='padding:1.5rem; text-align:center; color:#94A3B8; font-size:0.85rem;'>"
            "No sync history yet. Leads will appear here after being synced to HubSpot.</div>",
            unsafe_allow_html=True,
        )

    if st.button("Sync All Qualified Leads", type="primary", use_container_width=True, disabled=not hubspot_available):
        synced = 0
        for lead in leads:
            if lead.status == "Qualified" and lead.crm_synced == "No":
                result = crm_service.sync_lead(
                    lead.name, lead.email, lead.phone, lead.interest, lead.message or ""
                )
                if result.get("success"):
                    from database.db import get_session
                    from database.models import Lead as LeadModel
                    session = get_session()
                    db_lead = session.query(LeadModel).filter(LeadModel.id == lead.id).first()
                    if db_lead:
                        db_lead.crm_synced = "Yes"
                        session.commit()
                    session.close()
                    synced += 1
        if synced > 0:
            st.success(f"Synced {synced} lead(s) to HubSpot!")
            st.rerun()
        else:
            st.info("No qualified leads pending sync.")

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["settings"]} Connection Options</div>', unsafe_allow_html=True)

    provider = st.selectbox("CRM Provider", ["HubSpot", "Salesforce", "Zoho CRM", "Pipedrive"], disabled=not hubspot_available)
    api_key = st.text_input(
        "API Key",
        value=settings.HUBSPOT_ACCESS_TOKEN[:16] + "..." if settings.HUBSPOT_ACCESS_TOKEN else "",
        type="password",
        disabled=True,
    )

    st.toggle("Auto-create contact on new lead", value=True)
    st.toggle("Auto-create deal on qualified lead", value=True)
    st.toggle("Push conversation transcripts", value=False)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title" style="font-size:0.85rem;">{ICONS["book"]} Field Mapping</div>',
                unsafe_allow_html=True)
    mappings = [
        ("Chat visitor name", "Contact > First/Last Name"),
        ("Email captured by AI", "Contact > Email"),
        ("Lead score", "Contact > Lead Score"),
        ("Conversation transcript", "Deal > Notes"),
    ]
    for src, dst in mappings:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:space-between;
                        padding:0.5rem 0; border-bottom:1px solid #F1F5F9; font-size:0.8rem;">
                <span style="color:#374151;">{src}</span>
                <span style="color:#94A3B8;">→</span>
                <span style="color:#0F172A; font-weight:500;">{dst}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)