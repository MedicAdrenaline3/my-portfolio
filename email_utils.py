import requests
from config import Config

# === Email Provider Configuration ===
PROVIDER = Config.EMAIL_PROVIDER.lower()
RESEND_API_KEY = Config.RESEND_API_KEY
MAILERSEND_API_KEY = Config.MAILERSEND_API_KEY
RESEND_SENDER = Config.RESEND_SENDER
MAILERSEND_SENDER = Config.MAILERSEND_SENDER

# === API Endpoints ===
RESEND_URL = "https://api.resend.com/emails"
MAILERSEND_URL = "https://api.mailersend.com/v1/email"


def send_email(to_email, subject, content):
    """
    Sends an email using the configured provider (Resend or MailerSend).
    Automatically falls back to the secondary provider if the first fails.
    """
    to_list = [to_email] if isinstance(to_email, str) else to_email

    if PROVIDER == "resend":
        success = _send_via_resend(to_list, subject, content)
        if not success:
            print("[⚠️ Fallback] Resend failed — switching to MailerSend...")
            return _send_via_mailersend(to_list, subject, content)
        return True
    else:
        success = _send_via_mailersend(to_list, subject, content)
        if not success:
            print("[⚠️ Fallback] MailerSend failed — switching to Resend...")
            return _send_via_resend(to_list, subject, content)
        return True


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


def _send_via_mailersend(to_list, subject, content):
    """Private: Send email via MailerSend API (with detailed debug logging)."""
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

        # --- Debug logging ---
        if not response.ok:
            print(f"[❌ ERROR: MailerSend] Status {response.status_code}")
            try:
                error_info = response.json()
                print("[📨 MAILERSEND ERROR DETAILS]", error_info)
            except Exception:
                print("[📨 MAILERSEND RAW ERROR RESPONSE]", response.text)
            response.raise_for_status()

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
        "Best regards,\nMedic Adrenaline"
    )

    for email in recipient_emails:
        send_email(email, "Your Exam Practice PIN(s)", content)
