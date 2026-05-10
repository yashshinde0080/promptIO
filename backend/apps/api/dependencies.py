from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.auth_service import auth_service
from models.user import User, UserRole
from typing import Optional

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = await auth_service.get_current_user(credentials.credentials, db)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    from models.user import UserStatus
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )
    return current_user


def require_role(*roles: UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {[r.value for r in roles]}",
            )
        return current_user
    return role_checker


def require_admin():
    return require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)


def require_manager():
    return require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MANAGER)