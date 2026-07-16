"""
SafeX AI Lead Manager
Professional lead management table with search, filter, export CSV, delete, and CRM sync status.
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.utils import setup_page, ICONS, render_metric_row, export_csv
from database.queries import get_all_leads
from database.db import get_session
from database.models import Lead
from chatbot.lead_collection import LeadCollector

setup_page("Lead Manager", "leads")

# Status pill mapping
STATUS_PILL = {
    "New": "pill-blue",
    "Qualified": "pill-green",
    "Contacted": "pill-amber",
    "Lost": "pill-red",
}


@st.cache_data(ttl=30)
def load_leads():
    """Fetch leads from database with fallback to demo data."""
    try:
        leads = get_all_leads()
        return [
            {
                "id": lead.id,
                "name": lead.name or "Unknown",
                "email": lead.email or "",
                "phone": lead.phone or "",
                "source": lead.source or "Website",
                "status": lead.status or "New",
                "interest": lead.interest or "",
                "crm_synced": lead.crm_synced or "No",
                "score": max(20, min(100, hash(str(lead.id or lead.name)) % 81 + 20)),
                "created_at": lead.created_at.strftime("%Y-%m-%d %H:%M") if lead.created_at else "N/A",
            }
            for lead in leads
        ]
    except Exception:
        return [
            {"id": 1, "name": "Amara Khan", "email": "amara.khan@example.com", "phone": "+92301234567",
             "source": "Website Chat", "status": "New", "interest": "Product Demo", "crm_synced": "No",
             "score": 82, "created_at": "2026-07-15 14:30"},
            {"id": 2, "name": "Bilal Ahmed", "email": "bilal.a@example.com", "phone": "+92302234567",
             "source": "WhatsApp", "status": "Qualified", "interest": "Enterprise Plan", "crm_synced": "Yes",
             "score": 91, "created_at": "2026-07-15 11:20"},
            {"id": 3, "name": "Sana Tariq", "email": "sana.tariq@example.com", "phone": "+92303234567",
             "source": "Instagram DM", "status": "Contacted", "interest": "Pricing Info", "crm_synced": "No",
             "score": 64, "created_at": "2026-07-14 09:15"},
            {"id": 4, "name": "Usman Raza", "email": "usman.raza@example.com", "phone": "+92304234567",
             "source": "Email", "status": "New", "interest": "Support", "crm_synced": "No",
             "score": 55, "created_at": "2026-07-14 08:00"},
            {"id": 5, "name": "Zara Malik", "email": "zara.malik@example.com", "phone": "+92305234567",
             "source": "Website Chat", "status": "Qualified", "interest": "Premium Features", "crm_synced": "Yes",
             "score": 88, "created_at": "2026-07-13 16:45"},
            {"id": 6, "name": "Hamza Iqbal", "email": "hamza.i@example.com", "phone": "+92306234567",
             "source": "WhatsApp", "status": "Lost", "interest": "Price Concerns", "crm_synced": "No",
             "score": 21, "created_at": "2026-07-12 10:30"},
        ]


LEADS = load_leads()

# ---------- Top Stats ----------
render_metric_row([
    ("users", "#EEF2FF", "#4F46E5", "Total Leads", str(len(LEADS))),
    ("check", "#DCFCE7", "#166534", "Qualified", str(sum(1 for l in LEADS if l["status"] == "Qualified"))),
    ("clock", "#FEF3C7", "#92400E", "Awaiting Contact", str(sum(1 for l in LEADS if l["status"] == "New"))),
    ("trend-down", "#FEE2E2", "#991B1B", "Lost", str(sum(1 for l in LEADS if l["status"] == "Lost"))),
])

st.write("")

# ---------- Filters ----------
col_f1, col_f2, col_f3, col_f4 = st.columns([2, 1, 1, 1])

with col_f1:
    search = st.text_input("Search", placeholder="Search by name or email...", label_visibility="collapsed")

with col_f2:
    status_filter = st.selectbox(
        "Status", ["All", "New", "Qualified", "Contacted", "Lost"], label_visibility="collapsed"
    )

with col_f3:
    source_filter = st.selectbox(
        "Source", ["All", "Website Chat", "WhatsApp", "Email", "Instagram DM"], label_visibility="collapsed"
    )

with col_f4:
    # Sync CRM button
    if st.button("Sync to CRM", use_container_width=True, type="primary"):
        from services.crm import crm_service
        synced = 0
        for lead in LEADS:
            if lead["status"] == "Qualified" and lead["crm_synced"] == "No":
                result = crm_service.sync_lead(
                    lead["name"], lead["email"], lead["phone"],
                    lead["interest"], ""
                )
                if result.get("success"):
                    synced += 1
                    # Update DB
                    session = get_session()
                    db_lead = session.query(Lead).filter(Lead.id == lead["id"]).first()
                    if db_lead:
                        db_lead.crm_synced = "Yes"
                        session.commit()
                    session.close()
        if synced > 0:
            st.success(f"Synced {synced} lead(s) to HubSpot!")
            st.cache_data.clear()
        else:
            st.info("No qualified leads pending sync.")

st.write("")

# ---------- Filter Logic ----------
filtered = LEADS
if search:
    s = search.lower()
    filtered = [l for l in filtered if s in l["name"].lower() or s in l["email"].lower()]
if status_filter != "All":
    filtered = [l for l in filtered if l["status"] == status_filter]
if source_filter != "All":
    filtered = [l for l in filtered if l["source"] == source_filter]

# ---------- Leads Table ----------
st.markdown('<div class="panel">', unsafe_allow_html=True)

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(f'<div class="panel-title" style="margin-bottom:0;">{ICONS["users"]} Leads ({len(filtered)})</div>',
                unsafe_allow_html=True)
with header_col2:
    st.markdown(
        f"<div style='text-align:right; padding-top:4px;'>{export_csv(filtered, 'leads_export.csv')}</div>",
        unsafe_allow_html=True,
    )

if not filtered:
    st.markdown(
        "<div style='padding:2rem; text-align:center; color:#94A3B8; font-size:0.9rem;'>No leads match your filters.</div>",
        unsafe_allow_html=True,
    )
else:
    for lead in filtered:
        initials = "".join([p[0] for p in lead["name"].split()[:2]]).upper()
        pill_class = STATUS_PILL.get(lead["status"], "pill-gray")
        crm_pill = "pill-green" if lead["crm_synced"] == "Yes" else "pill-amber"

        st.markdown(
            f"""
            <div class="row-card">
                <div style="display:flex; align-items:center; gap:12px; flex:2;">
                    <div class="avatar">{initials}</div>
                    <div>
                        <div style="font-weight:600; color:#0F172A; font-size:0.88rem;">{lead['name']}</div>
                        <div style="font-size:0.78rem; color:#64748B;">{lead['email']} · {lead['phone']}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:12px; flex:1;">
                    <div style="font-size:0.78rem; color:#64748B;">{lead['interest'][:20]}</div>
                </div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <span class="pill {pill_class}">{lead['status']}</span>
                    <div>
                        <div class="score-bar">
                            <div class="score-bar-fill" style="width:{lead['score']}%;
                                background:{'#166534' if lead['score'] >= 80 else '#D97706' if lead['score'] >= 50 else '#DC2626'};">
                            </div>
                        </div>
                        <div style="font-size:0.65rem; color:#64748B; text-align:center;">{lead['score']}</div>
                    </div>
                    <span class="pill {crm_pill}" style="font-size:0.6rem;">CRM</span>
                    <span style="font-size:0.72rem; color:#94A3B8;">{lead['source']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Add New Lead Form ----------
st.write("")
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown(f'<div class="panel-title">{ICONS["plus"]} Capture New Lead</div>', unsafe_allow_html=True)

with st.form("new_lead_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        lead_name = st.text_input("Full name", placeholder="Amara Khan")
        lead_email = st.text_input("Email", placeholder="amara@example.com")
    with c2:
        lead_phone = st.text_input("Phone", placeholder="+92 300 1234567")
        lead_source = st.selectbox("Source", ["Website Chat", "WhatsApp", "Email", "Instagram DM", "Other"])

    lead_interest = st.text_input("Interest / Product", placeholder="e.g., Enterprise Plan, Pricing Info")
    lead_message = st.text_area("Notes", placeholder="Any additional information...", height=80)

    submitted = st.form_submit_button("Add Lead", type="primary", use_container_width=True)

    if submitted:
        collector = LeadCollector()
        if not lead_name.strip():
            st.error("Name is required")
        elif not lead_email or not collector.valid_email(lead_email):
            st.error("Valid email is required")
        elif lead_phone and not collector.valid_phone(lead_phone):
            st.error("Phone number must be at least 10 digits")
        else:
            collector.save(lead_name, lead_email, lead_phone, lead_interest, lead_message, source=lead_source)
            st.success(f"Lead '{lead_name}' added successfully!")
            st.cache_data.clear()

st.markdown("</div>", unsafe_allow_html=True)