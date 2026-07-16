"""
SafeX AI Chat Interface
Enterprise AI-powered customer support conversation page.
Features: conversation history, source badges, confidence display, typing animation,
clear conversation, export chat, session info, database logging.
"""

import streamlit as st
from datetime import datetime
import sys
import os
import uuid
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.utils import setup_page, ICONS, source_badge, confidence_pill, typing_animation, export_csv
from chatbot.router import Router
from database.queries import log_chat, get_all_conversations

setup_page("Chat", "chat")

# Initialize Router for message routing and response generation
@st.cache_resource
def get_router():
    return Router()

router = get_router()

# Session state initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "text": "Hi! I'm the SafeX AI assistant. Ask me anything about your account, orders, or integrations.",
            "time": datetime.now().strftime("%I:%M %p"),
            "source": "Greeting",
            "confidence": 1.0,
        }
    ]

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# Layout: Chat on left, session info on right
left_col, right_col = st.columns([2.4, 1])

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="panel-title" style="display:flex; align-items:center; justify-content:space-between;">'
        f'<span>{ICONS["bot"]} Live Conversation</span>'
        f'<span style="display:flex; gap:6px;">'
        f'<button class="btn-ghost btn-sm" onclick="document.querySelector(\'[data-testid=\\\'baseButton-secondary\\\']\').click()" style="padding:0.3rem 0.6rem;">{ICONS["trash"]} Clear</button>'
        f'</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Chat messages container
    chat_box = st.container(height=440, border=False)
    with chat_box:
        for idx, m in enumerate(st.session_state.messages):
            role_class = "user" if m["role"] == "user" else "assistant"
            align = "user" if m["role"] == "user" else ""

            # Build message HTML
            msg_html = f"""
            <div class="msg-row {align}">
                <div>
                    <div class="msg-bubble {role_class}">{m['text']}</div>
                    <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
                        <div class="msg-meta {'user-meta' if m['role'] == 'user' else ''}">{m['time']}</div>
            """
            if m["role"] == "assistant" and m.get("source"):
                msg_html += source_badge(m.get("source", ""))
            if m["role"] == "assistant" and m.get("confidence") is not None:
                msg_html += confidence_pill(m.get("confidence"))
            msg_html += """
                    </div>
                </div>
            </div>
            """
            st.markdown(msg_html, unsafe_allow_html=True)

        # Show typing indicator when waiting
        if st.session_state.waiting_for_response:
            st.markdown(
                f'<div class="msg-row"><div><div class="msg-bubble assistant">{typing_animation()}</div></div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Chat input using st.chat_input for clean rendering (no extra form divs)
    user_input = st.chat_input("Type your message here...", key="chat_input")

    # Handle message submission
    if user_input and user_input.strip():
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({
            "role": "user",
            "text": user_input,
            "time": now,
        })
        st.session_state.waiting_for_response = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Process response outside form to avoid rerun issues
    if st.session_state.waiting_for_response:
        user_msg = st.session_state.messages[-1]["text"]
        now = datetime.now().strftime("%I:%M %p")

        try:
            response = router.reply(st.session_state.session_id, user_msg)
            bot_reply = response.get("answer", "I'm sorry, I couldn't process that.")
            source = response.get("source", "AI")
            confidence = response.get("confidence", 0)

            # Log user message
            log_chat(
                session_id=st.session_state.session_id,
                role="user",
                message=user_msg,
                language="en",
                intent="user_query",
                matched_question=response.get("matched_question"),
                similarity=confidence,
                answered_by=source,
                response_time=0,
            )

            # Log bot response
            log_chat(
                session_id=st.session_state.session_id,
                role="assistant",
                message=bot_reply,
                language="en",
                intent="ai_response",
                matched_question=response.get("matched_question"),
                similarity=confidence,
                answered_by=source,
                response_time=0,
            )

            st.session_state.messages.append({
                "role": "assistant",
                "text": bot_reply,
                "time": now,
                "source": source,
                "confidence": confidence,
            })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "text": f"Error processing your message. Please try again.",
                "time": now,
                "source": "Error",
                "confidence": 0,
            })

        st.session_state.waiting_for_response = False
        st.rerun()

    # Clear conversation button
    if st.button("Clear Conversation", key="clear_chat_btn"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "text": "Hi! I'm the SafeX AI assistant. Ask me anything about your account, orders, or integrations.",
                "time": datetime.now().strftime("%I:%M %p"),
                "source": "Greeting",
                "confidence": 1.0,
            }
        ]
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    # Export Chat
    if st.session_state.messages:
        export_data = [
            {
                "role": m["role"],
                "message": m["text"],
                "time": m["time"],
                "source": m.get("source", ""),
                "confidence": m.get("confidence", ""),
            }
            for m in st.session_state.messages
        ]
        st.markdown(
            export_csv(export_data, f"chat_export_{st.session_state.session_id[:8]}.csv"),
            unsafe_allow_html=True,
        )

# Right sidebar - Session Info
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["info"]} Session</div>', unsafe_allow_html=True)

    # Session stats
    msg_count = len(st.session_state.messages)
    bot_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    user_msgs = msg_count - bot_msgs

    st.markdown(
        f"""
        <div style="font-size:0.85rem; color:#374151; line-height:2.2;">
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">Session ID</span>
            <span style="font-weight:500; font-size:0.78rem;">{st.session_state.session_id[:12]}...</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">Messages</span>
            <span style="font-weight:600;">{msg_count}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">User</span>
            <span style="font-weight:600;">{user_msgs}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">AI Responses</span>
            <span style="font-weight:600;">{bot_msgs}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">Channel</span>
            <span style="font-weight:500;">Website Widget</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#64748B;">Status</span>
            <span class="pill pill-green">Active</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Suggested FAQs
    st.markdown('<div class="panel" style="margin-top:0.75rem;">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{ICONS["book"]} Suggested FAQs</div>', unsafe_allow_html=True)
    faq_suggestions = [
        "How do refunds work?",
        "Where's my order?",
        "How do I reset my password?",
        "What are your business hours?",
        "How do I contact support?",
    ]
    for q in faq_suggestions:
        st.markdown(
            f"""<div class="row-card" style="padding:0.6rem 0.9rem; margin-bottom:4px; cursor:pointer;"
                      onclick="document.querySelector('[data-testid=\\'stChatInput\\'] textarea').value = '{q.replace("'", "\\'")}';">
                <span style="font-size:0.82rem; color:#374151;">{q}</span>
                {ICONS["search"]}
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)