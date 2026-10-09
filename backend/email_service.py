import html
import os

import resend

from backend.schemas import ContactMessage


async def send_contact_email(contact: ContactMessage) -> None:
    """Send a portfolio contact message through the Resend HTTPS API."""

    resend_api_key = os.getenv("RESEND_API_KEY")
    destination_email = os.getenv("CONTACT_TO_EMAIL")

    if not resend_api_key:
        raise RuntimeError("RESEND_API_KEY environment variable is missing.")

    if not destination_email:
        raise RuntimeError("CONTACT_TO_EMAIL environment variable is missing.")

    resend.api_key = resend_api_key

    # Prevent line breaks in the email subject.
    first_name = contact.first_name.replace("\n", " ").replace("\r", " ").strip()
    last_name = contact.last_name.replace("\n", " ").replace("\r", " ").strip()

    company = contact.company.strip() if contact.company else "Not specified"

    # Escape user-provided values before inserting them into HTML.
    safe_first_name = html.escape(contact.first_name)
    safe_last_name = html.escape(contact.last_name)
    safe_email = html.escape(str(contact.email))
    safe_company = html.escape(company)
    safe_message = html.escape(contact.message).replace("\n", "<br>")

    params: resend.Emails.SendParams = {
        "from": "Portfolio <contact@tommouquet.com>",
        "to": [destination_email],
        "reply_to": str(contact.email),
        "subject": f"Portfolio — New message from {first_name} {last_name}",
        "html": f"""
        <h2>New message received from your portfolio.</h2>

        <p>
            <strong>First name:</strong><br>
            {safe_first_name}
        </p>

        <p>
            <strong>Last name:</strong><br>
            {safe_last_name}
        </p>

        <p>
            <strong>Email:</strong><br>
            {safe_email}
        </p>

        <p>
            <strong>Company:</strong><br>
            {safe_company}
        </p>

        <p>
            <strong>Message:</strong><br>
            {safe_message}
        </p>
        """.strip(),
        "text": f"""
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
""".strip(),
    }

    await resend.Emails.send_async(params)
