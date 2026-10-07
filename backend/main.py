import logging
import os

from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.email_service import send_contact_email
from backend.schemas import ContactMessage


logger = logging.getLogger(__name__)



SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
CONTACT_TO_EMAIL = os.getenv("CONTACT_TO_EMAIL")

if not SMTP_USER or not SMTP_APP_PASSWORD or not CONTACT_TO_EMAIL:
    raise RuntimeError("Missing email environment variables.")


app = FastAPI(
    title="Portfolio Contact API",
    version="1.0.0",
)


default_origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://tom-mouquet-portfolio.onrender.com",
]


configured_origins = os.getenv("FRONTEND_ORIGINS")

if configured_origins:
    allowed_origins = [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]
else:
    allowed_origins = default_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/contact",
    status_code=status.HTTP_201_CREATED,
)
def submit_contact_form(contact: ContactMessage):
    try:
        send_contact_email(contact)

    except Exception:
        logger.exception("Unable to send contact email")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to send message.",
        )

    return {
        "message": "Message sent successfully."
    }
