from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole, UserStatus


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: UserRole
    status: UserStatus
    organization_id: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    is_email_verified: bool
    is_mfa_enabled: bool
    last_login_at: Optional[datetime]
    login_count: int
    gdpr_consent: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserAdminUpdateRequest(BaseModel):
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    organization_id: Optional[str] = None