from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


ShortText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

MessageText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=5000,
    ),
]


class ContactMessage(BaseModel):
    first_name: ShortText
    last_name: ShortText
    email: EmailStr
    company: ShortText | None = None
    message: MessageText
