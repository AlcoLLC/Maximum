import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request, AuthorizedSession
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)
JSON_KEY_FILE_NAME = 'maximu-475808-deb81cf7805e.json' 
JSON_KEY_FILE = getattr(settings, 'GOOGLE_INDEXING_KEY_FILE', 
                        os.path.join(settings.BASE_DIR, JSON_KEY_FILE_NAME))

API_SCOPE = 'https://www.googleapis.com/auth/indexing'
ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

def get_credentials():
    try:
        creds = service_account.Credentials.from_service_account_file(
            JSON_KEY_FILE, scopes=[API_SCOPE])
        if not creds.valid:
            creds.refresh(Request())
        return creds
    except FileNotFoundError:
        logger.error(f"[Google Indexing] HATA: JSON anahtar dosyası bulunamadı: {JSON_KEY_FILE}")
        return None
    except Exception as e:
        logger.error(f"[Google Indexing] Kimlik bilgileri alınırken hata: {e}", exc_info=True)
        return None

def submit_url_to_google(url_to_submit, url_type="URL_UPDATED"):
    credentials = get_credentials()
    if not credentials:
        logger.warning(f"[Google Indexing] Kimlik bilgisi yok, {url_to_submit} gönderilemedi.")
        return

    session = AuthorizedSession(credentials)
    
    payload = {
        "url": url_to_submit,
        "type": url_type
    }

    try:
        response = session.post(ENDPOINT, json=payload)
        response.raise_for_status() 
        logger.info(f"[Google Indexing] Başarılı ({url_type}): {url_to_submit}")

    except requests.exceptions.HTTPError as e:
        try:
            error_json = e.response.json()
            error_message = error_json.get("error", {}).get("message", e.response.text)
        except requests.exceptions.JSONDecodeError:
            error_message = e.response.text
        logger.error(f"[Google Indexing] HATA ({e.response.status_code}) {url_to_submit}: {error_message}")
    except Exception as e:
        logger.error(f"[Google Indexing] BEKLENMEDİK HATA {url_to_submit}: {e}", exc_info=True)