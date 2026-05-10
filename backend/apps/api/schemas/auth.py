from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import datetime
import re


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    organization_name: Optional[str] = None
    gdpr_consent: bool = False

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]{3,50}$", v):
            raise ValueError(
                "Username must be 3-50 characters and contain only letters, numbers, underscores, hyphens"
            )
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @model_validator(mode="after")
    def validate_gdpr_consent(self) -> "RegisterRequest":
        if not self.gdpr_consent:
            raise ValueError("GDPR consent is required to create an account")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserMinimal"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserMinimal(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    organization_id: Optional[str] = None

    class Config:
        from_attributes = True