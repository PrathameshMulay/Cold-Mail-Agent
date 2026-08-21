from pydantic import BaseModel


class ColdEmail(BaseModel):
    subject: str
    body: str