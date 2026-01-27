import imaplib
import email
from email.header import decode_header
import os

class EmailService:
    def __init__(self):
        self.host = os.getenv("IMAP_HOST", "imap.gmail.com")
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS") # Use App Password para Gmail

    def fetch_latest_emails(self, limit=10):
        if not self.user or not self.password:
            return []

        try:
            # Conecta ao servidor IMAP
            mail = imaplib.IMAP4_SSL(self.host)
            mail.login(self.user, self.password)
            mail.select("inbox")

            # Busca os IDs dos emails mais recentes
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()
            
            latest_ids = email_ids[-limit:]
            latest_ids.reverse() # Mais recentes primeiro

            emails_list = []
            for e_id in latest_ids:
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode Subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        
                        # Decode From
                        from_, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(from_, bytes):
                            from_ = from_.decode(encoding or "utf-8")

                        # Extract Body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        emails_list.append({
                            "id": e_id.decode(),
                            "subject": subject,
                            "sender": from_,
                            "text": body[:5000],
                            "date": msg.get("Date")
                        })

            mail.logout()
            return emails_list
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
