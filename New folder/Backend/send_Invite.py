import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def send_interview_invitation(recipient_email: str, interview_date: str, interview_time: str):
    """
    Sends an interview invitation to the specified recipient.
    """
    # Replace these environment variables or set them via your shell / config
    # e.g. export GMAIL_USER="yourgmail@gmail.com"
    #      export GMAIL_PASSWORD="yourgmailpassword" (or app-specific password)
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_password = os.environ.get("GMAIL_PASSWORD")

    if not gmail_user or not gmail_password:
        raise ValueError("Gmail credentials are not set in environment variables.")

    # Construct the subject and body
    subject = "Interview Invitation"
    body = (
        f"Hello,\n\n"
        f"Thank you for your application. We would love to invite you for an interview!\n\n"
        f"Date: {interview_date}\n"
        f"Time: {interview_time}\n\n"
        f"Please reply to confirm your availability. We look forward to meeting you!\n\n"
        f"Best regards,\n"
        f"Your Company"
    )

    # Create the email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient_email
    msg.set_content(body)

    # Send via Gmail SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        print("Interview invitation sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
