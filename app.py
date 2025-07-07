# app.py

import streamlit as st
import pandas as pd
import time
from enrich import enrich_company
from classify import classify_industry
from emailgen import generate_email
from gmail_send import gmail_authenticate, send_email

st.set_page_config(page_title="🚀 LeadGenius AI", layout="wide")
st.title("📈 LeadGenius AI — Smarter Outreach with Enriched Leads")

# Global Gmail service session
service = None

# Step 1: Upload CSV
uploaded_file = st.file_uploader("📤 Upload a CSV file with a 'company' column", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Companies:")
    st.dataframe(df)

    # Step 2: Website Enrichment + Classification
    if st.button("🔍 Enrich with Website + Industry"):
        enriched_data = []

        with st.spinner("🧠 Processing companies..."):
            for name in df["company"]:
                site, snippet = enrich_company(name)
                industry, confidence = classify_industry(snippet)

                enriched_data.append({
                    "company": name,
                    "website": site,
                    "snippet": snippet,
                    "industry": industry,
                    "confidence": confidence
                })
                time.sleep(2)

        result_df = pd.DataFrame(enriched_data)
        st.session_state["enriched_df"] = result_df

        st.success("✅ Done! Here's your enriched lead data:")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "enriched_leads.csv", "text/csv")

# Step 3: Authenticate Gmail
if st.button("🔐 Connect Gmail Account"):
    try:
        service = gmail_authenticate()
        st.session_state["gmail_service"] = service
        st.success("✅ Gmail authenticated successfully.")
    except Exception as e:
        st.error(f"❌ Gmail authentication failed: {e}")

# Step 4: Cold Email Generator + Sender
if "enriched_df" in st.session_state:
    st.subheader("📩 Cold Email Generator + One-Click Gmail Send")
    enriched_df = st.session_state["enriched_df"]
    service = st.session_state.get("gmail_service")

    for idx, row in enriched_df.iterrows():
        email_text = generate_email(row["company"], row["industry"], row["snippet"])
        with st.expander(f"✉️ Email to {row['company']}"):
            st.code(email_text, language="markdown")
            to_email = st.text_input(f"📧 Enter recipient email for {row['company']}", key=f"email_{idx}")

            if service and st.button(f"📤 Send Email to {row['company']}", key=f"send_{idx}"):
                try:
                    send_email(
                        service=service,
                        sender="me",
                        to=to_email,
                        subject=f"Exploring Synergies with {row['company']}",
                        message_text=email_text
                    )
                    st.success(f"✅ Email sent to {to_email}")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")