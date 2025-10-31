import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # === General Configuration ===
    SECRET_KEY = os.getenv('SECRET_KEY')

    # === Database Configuration ===
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"ssl": {"fake_flag_to_enable_ssl": True}}
    }

    # === Payment & Contact ===
    PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
    PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
    WHATSAPP_LINK = os.getenv('WHATSAPP_LINK')

    # === AI & External APIs ===
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

    # === Email Configuration ===
    # 1️⃣ Primary: Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    RESEND_SENDER = os.getenv("RESEND_SENDER", "JAMB OTP <adrena-jamb-cbt@adrena-jamb-cbt.buzz>")

    # 2️⃣ Secondary: SendGrid
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDGRID_SENDER = os.getenv("SENDGRID_SENDER", "JAMB OTP <adrena-jamb-cbt@adrena-jamb-cbt.buzz>")

    # 3️⃣ Tertiary: MailerSend
    MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
    MAILERSEND_SENDER = os.getenv("MAILERSEND_SENDER", "JAMB OTP <adrena-jamb-cbt@adrena-jamb-cbt.buzz>")
    
    # === Default provider logic ===
    # Options: "resend", "sendgrid", or "mailersend"
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "resend")

    # === Convenience (not required but helpful for debugging)
    EMAIL_PROVIDERS = {
        "resend": {
            "api_key": RESEND_API_KEY,
            "sender": RESEND_SENDER,
            "base_url": "https://api.resend.com/emails"
        },
        "sendgrid": {
            "api_key": SENDGRID_API_KEY,
            "sender": SENDGRID_SENDER,
            "base_url": "https://api.sendgrid.com/v3/mail/send"
        },
        "mailersend": {
            "api_key": MAILERSEND_API_KEY,
            "sender": MAILERSEND_SENDER,
            "base_url": "https://api.mailersend.com/v1/email"
        }
    }

    # Fallback values (mostly unused now but kept for legacy)
    MAIL_SERVER = "api.resend.com"
    MAIL_PORT = 443
    MAIL_USE_TLS = True
    MAIL_USERNAME = RESEND_SENDER
    MAIL_PASSWORD = RESEND_API_KEY
