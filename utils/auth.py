import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import link

def authenticate(url = link.BASESHEET):
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    path = './config.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, gss_scopes)
    gss_client = gspread.authorize(credentials)
    sheet = gss_client.open_by_url(url)
    return sheet