import os
import smtplib
import ssl
from email.message import EmailMessage

from backend.schemas import ContactMessage


def send_contact_email(contact: ContactMessage) -> None:
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_APP_PASSWORD")
    destination_email = os.getenv("CONTACT_TO_EMAIL", smtp_user)

    if not smtp_user:
        raise RuntimeError("SMTP_USER environment variable is missing.")

    if not smtp_password:
        raise RuntimeError("SMTP_APP_PASSWORD environment variable is missing.")

    if not destination_email:
        raise RuntimeError("CONTACT_TO_EMAIL environment variable is missing.")

    # Évite qu'un utilisateur injecte des retours à la ligne
    # dans le sujet du mail.
    first_name = contact.first_name.replace("\n", " ").replace("\r", " ")
    last_name = contact.last_name.replace("\n", " ").replace("\r", " ")

    company = contact.company or "Not specified"

    email = EmailMessage()

    email["Subject"] = (
        f"Portfolio — New message from {first_name} {last_name}"
    )

    # Le mail est techniquement envoyé depuis ton propre compte Gmail.
    email["From"] = smtp_user
    email["To"] = destination_email

    # Mais quand tu cliques sur "Répondre",
    # Gmail utilisera l'adresse du visiteur.
    email["Reply-To"] = str(contact.email)

    email.set_content(
        f"""
New message received from your portfolio.

First name:
{contact.first_name}

Last name:
{contact.last_name}

Email:
{contact.email}

Company:
{company}

Message:
{contact.message}
""".strip()
    )

    ssl_context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=ssl_context,
    ) as smtp:
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(email)
