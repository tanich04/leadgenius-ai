import base64
import json
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None

    # Load from session if already authenticated
    if "token" in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state["token"], SCOPES)
        return build('gmail', 'v1', credentials=creds)

    # Create flow manually using client config from secrets
    flow = Flow.from_client_config(
        json.loads(st.secrets["GOOGLE_CREDENTIALS"]),
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # <== THIS is key
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"🔐 **[Click here to authorize Gmail]({auth_url})**")

    code = st.text_input("📥 Paste the authorization code here to complete login:")

    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials
            st.session_state["token"] = json.loads(creds.to_json())
            st.success("✅ Gmail authenticated!")
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            st.error(f"❌ Authentication failed: {e}")
            st.stop()
    else:
        st.info("Paste the code after clicking the link above.")
        st.stop()


def send_email(service, sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    return service.users().messages().send(userId="me", body=body).execute()
