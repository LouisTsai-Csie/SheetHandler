import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import link
import streamlit as st

def authenticate(url):
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    credentials_info = {
        "type": "service_account",
        "project_id": st.secrets['project_id'],
        "private_key_id": st.secrets['private_key_id'],
        "private_key": st.secrets['private_key'],
        "client_email": st.secrets['client_email'],
        "client_id": st.secrets['client_id'],
        "auth_uri": st.secrets['auth_uri'],
        "token_uri": st.secrets['token_uri'],
        "auth_provider_x509_cert_url": st.secrets['auth_provider_x509_cert_url'],
        "client_x509_cert_url": st.secrets['client_x509_cert_url']
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, gss_scopes)
    gss_client = gspread.authorize(credentials)
    sheet = gss_client.open_by_url(url)
    return sheet
