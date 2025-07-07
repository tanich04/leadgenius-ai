import base64
import json
import os
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None

    # Try loading saved credentials from session
    if "token" in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state["token"], SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(
            json.loads(st.secrets["GOOGLE_CREDENTIALS"]),
            SCOPES
        )

        auth_url, _ = flow.authorization_url(prompt='consent')
        st.info("🔐 Please [click here to authorize Gmail]({})".format(auth_url))
        code = st.text_input("Paste the authorization code here:")

        if code:
            try:
                flow.fetch_token(code=code)
                creds = flow.credentials
                st.session_state["token"] = json.loads(creds.to_json())
                st.success("✅ Gmail authenticated successfully.")
                return build('gmail', 'v1', credentials=creds)
            except Exception as e:
                st.error(f"❌ Authentication failed: {e}")
                return None
        else:
            st.stop()

    return build('gmail', 'v1', credentials=creds)


def send_email(service, sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    return service.users().messages().send(userId="me", body=body).execute()
