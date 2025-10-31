import requests
from config import Config

# === Email Provider Configuration ===
PROVIDER = Config.EMAIL_PROVIDER.lower()

# Provider credentials
RESEND_API_KEY = Config.RESEND_API_KEY
MAILERSEND_API_KEY = Config.MAILERSEND_API_KEY
SENDGRID_API_KEY = Config.SENDGRID_API_KEY

# Sender emails
RESEND_SENDER = Config.RESEND_SENDER
MAILERSEND_SENDER = Config.MAILERSEND_SENDER
SENDGRID_SENDER = Config.SENDGRID_SENDER

# API endpoints
RESEND_URL = "https://api.resend.com/emails"
MAILERSEND_URL = "https://api.mailersend.com/v1/email"
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


# === Universal Email Function with Fallbacks ===
def send_email(to_email, subject, content):
    """
    Sends an email using the configured provider (Resend → SendGrid → MailerSend fallback).
    """
    to_list = [to_email] if isinstance(to_email, str) else to_email

    print(f"\n[📨 Attempting to send email to {to_list}]")

    # 1️⃣ Try Resend
    if _send_via_resend(to_list, subject, content):
        return True

    # 2️⃣ Fallback to SendGrid
    print("[⚠️ Fallback] Resend failed — switching to SendGrid...")
    if _send_via_sendgrid(to_list, subject, content):
        return True

    # 3️⃣ Final fallback to MailerSend
    print("[⚠️ Fallback] SendGrid failed — switching to MailerSend...")
    return _send_via_mailersend(to_list, subject, content)


# === Provider Implementations ===

def _send_via_resend(to_list, subject, content):
    """Private: Send email via Resend API."""
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "from": RESEND_SENDER,
        "to": to_list,
        "subject": subject,
        "text": content,
    }

    try:
        response = requests.post(RESEND_URL, headers=headers, json=data)
        response.raise_for_status()
        print(f"[✅ SUCCESS: Resend] Email sent to {to_list}")
        return True
    except Exception as e:
        print(f"[❌ ERROR: Resend] {e}")
        return False


def _send_via_sendgrid(to_list, subject, content):
    """Private: Send email via SendGrid API."""
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    # Build SendGrid JSON structure
    data = {
        "personalizations": [{"to": [{"email": email} for email in to_list]}],
        "from": {"email": SENDGRID_SENDER.split('<')[-1].strip('>')},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content}],
    }

    try:
        response = requests.post(SENDGRID_URL, headers=headers, json=data)
        if response.status_code not in (200, 202):
            print(f"[❌ ERROR: SendGrid] Status {response.status_code}")
            try:
                print("[📨 SENDGRID ERROR DETAILS]", response.json())
            except Exception:
                print("[📨 SENDGRID RAW ERROR]", response.text)
            return False

        print(f"[✅ SUCCESS: SendGrid] Email sent to {to_list}")
        return True
    except Exception as e:
        print(f"[❌ EXCEPTION: SendGrid] {e}")
        return False


def _send_via_mailersend(to_list, subject, content):
    """Private: Send email via MailerSend API."""
    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "from": {"email": MAILERSEND_SENDER.split('<')[-1].strip('>')},
        "to": [{"email": email} for email in to_list],
        "subject": subject,
        "text": content,
    }

    try:
        response = requests.post(MAILERSEND_URL, headers=headers, json=data)
        if not response.ok:
            print(f"[❌ ERROR: MailerSend] Status {response.status_code}")
            try:
                print("[📨 MAILERSEND ERROR DETAILS]", response.json())
            except Exception:
                print("[📨 MAILERSEND RAW ERROR RESPONSE]", response.text)
            return False

        print(f"[✅ SUCCESS: MailerSend] Email sent to {to_list}")
        return True
    except Exception as e:
        print(f"[❌ EXCEPTION: MailerSend] {e}")
        return False


# === Predefined Email Templates ===

def send_otp_email(to_email, otp):
    """Send OTP verification email."""
    content = (
        f"Hi,\n\n"
        f"Your OTP is: {otp}\n\n"
        f"Best regards,\nMedic Adrenaline"
    )
    send_email(to_email, "Verify Your Exam Practice Account", content)


def send_reset_password_email(to_email, token):
    """Send password reset email."""
    content = (
        f"Hi,\n\n"
        f"Your password reset token is: {token}\n\n"
        f"This token will expire in 1 hour.\n\n"
        f"Best regards,\nMedic Adrenaline"
    )
    send_email(to_email, "Password Reset Request", content)


def send_exam_pins_email(to_email, pins_dict):
    """Send PINs for a single recipient."""
    content = "Hi,\n\nHere are your PINs:\n\n"
    for mode, pin in pins_dict.items():
        content += f"- {mode}: {pin}\n"
    content += (
        "\nNote: Do not disclose your PIN. Once activated, it’s tied to your device.\n"
        "Contact the admin via the login page if you need to access your account on another device.\n\n"
        "Best regards,\nMedic Adrenaline"
    )
    send_email(to_email, "Your Exam Practice PIN(s)", content)


def send_exam_pins_email_bulk(recipient_emails, pins_dict):
    """Send the same PIN info to multiple recipients."""
    content = "Dear Student,\n\nHere are your PIN(s):\n\n"
    for mode, pin in pins_dict.items():
        content += f"{mode.upper()} PIN: {pin}\n"
    content += (
        "\nNote: Do not disclose your PIN. Once activated, it’s tied to your device.\n"
        "Contact the admin via the login page if you need to access your account on another device.\n\n"
        "Best regards,\nMedic Adrenaline Team"
    )

    for email in recipient_emails:
        send_email(email, "Your Exam Practice PIN(s)", content)