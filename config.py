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
    # Primary: Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    RESEND_SENDER = os.getenv("RESEND_SENDER", "JAMB OTP <adrena-jamb-cbt@adrena-jamb-cbt.buzz>")

    # Secondary: MailerSend
    MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
    MAILERSEND_SENDER = os.getenv("MAILERSEND_SENDER", "JAMB OTP <adrena-jamb-cbt@adrena-jamb-cbt.buzz>")

    # Default settings (Resend first)
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "resend")  # "resend" or "mailersend"

    # Fallback SMTP-style values for compatibility
    MAIL_SERVER = "api.resend.com" if EMAIL_PROVIDER == "resend" else "api.mailersend.com"
    MAIL_PORT = 443
    MAIL_USE_TLS = True
    MAIL_USERNAME = RESEND_SENDER if EMAIL_PROVIDER == "resend" else MAILERSEND_SENDER
    MAIL_PASSWORD = RESEND_API_KEY if EMAIL_PROVIDER == "resend" else MAILERSEND_API_KEY
