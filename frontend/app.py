import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="🦊 MailFox")

st.title("🦊 MailFox — AI Email Assistant")

# -----------------------------
# Session State Init
# -----------------------------
if "inbox" not in st.session_state:
    st.session_state.inbox = []

if "selected_email" not in st.session_state:
    st.session_state.selected_email = None

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "reply" not in st.session_state:
    st.session_state.reply = ""

# -----------------------------
# Load Inbox Button
# -----------------------------
if st.button("🔄 Load Inbox"):
    with st.spinner("Fetching unread Gmail emails..."):
        try:
            res = requests.get(f"{BACKEND_URL}/gmail/inbox")

            if res.status_code != 200:
                st.error("❌ Backend not reachable")
            else:
                data = res.json()
                if data.get("success"):
                    st.session_state.inbox = data.get("emails", [])
                else:
                    st.error("❌ Backend error while fetching inbox.")
                    st.code(data.get("error", "Unknown error"))

        except Exception as e:
            st.error("❌ Failed to connect to backend.")

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns([3, 7])

# -----------------------------
# LEFT: Inbox
# -----------------------------
with col1:
    st.subheader("📥 Inbox")

    if not st.session_state.inbox:
        st.info("Click **Load Inbox** to fetch unread emails.")
    else:
        for i, email in enumerate(st.session_state.inbox):
            if st.button(
                f"{email['from']} — {email['subject']}",
                key=f"email_{i}"
            ):
                st.session_state.selected_email = email
                st.session_state.summary = ""
                st.session_state.reply = ""

# -----------------------------
# RIGHT: Email Viewer
# -----------------------------
with col2:
    st.subheader("📄 Email Viewer")

    email = st.session_state.selected_email

    if email is None:
        st.info("Select an email from the inbox.")
    else:
        st.markdown(f"**From:** {email['from']}")
        st.markdown(f"**Subject:** {email['subject']}")
        st.divider()
        st.write(email["body"])

        email_text = email["body"]

        # -----------------------------
        # Summarize
        # -----------------------------
        if st.button("📝 Summarize Email"):
            with st.spinner("Summarizing email..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/summarize",
                        json={"email_text": email_text},
                        timeout=60
                    )

                    if res.status_code == 200:
                        st.session_state.summary = res.json().get("summary", "")
                    else:
                        st.error("❌ Failed to summarize email.")

                except Exception:
                    st.error("❌ AI service not reachable.")

        if st.session_state.summary:
            st.subheader("🧠 AI Summary")
            st.success(st.session_state.summary)

        # -----------------------------
        # Generate Reply
        # -----------------------------
        if st.button("✍️ Generate Reply"):
            with st.spinner("Generating reply..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/reply",
                        json={"email_text": email_text},
                        timeout=60
                    )

                    if res.status_code == 200:
                        st.session_state.reply = res.json().get("reply", "")
                    else:
                        st.error("❌ Failed to generate reply.")

                except Exception:
                    st.error("❌ AI service not reachable.")

        if st.session_state.reply:
            st.subheader("📨 AI Reply")
            st.text_area(
                "Reply text",
                st.session_state.reply,
                height=220
            )
