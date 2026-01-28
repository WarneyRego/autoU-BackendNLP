import os
from dotenv import load_dotenv
import sys
sys.path.append('src')
from email_service import EmailService

load_dotenv()

def test_email():
    print("Testing EmailService...")
    print(f"User: {os.getenv('EMAIL_USER')}")
    srv = EmailService()
    emails = srv.fetch_latest_emails(limit=3)
    print(f"Fetched {len(emails)} emails")
    for e in emails:
        print(f"Subject: {e['subject']}")

if __name__ == "__main__":
    test_email()
