from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshTokenRequest, ChangePasswordRequest, UserMinimal
)
from services.auth_service import auth_service
from services.audit_service import audit_service
from models.audit import AuditAction
from dependencies import get_current_active_user
from models.user import User
from utils.helpers import get_client_ip
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Register new user account with GDPR consent"""
    try:
        user, organization = await auth_service.register(data, db)

        access_token = auth_service.create_access_token(
            str(user.id),
            user.role.value,
            str(user.organization_id) if user.organization_id else None,
        )
        refresh_token = auth_service.create_refresh_token(str(user.id))

        await audit_service.log(
            db=db,
            action=AuditAction.USER_REGISTER,
            user_id=str(user.id),
            organization_id=str(user.organization_id) if user.organization_id else None,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get("user-agent"),
            details={"email": user.email},
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=60 * 60,
            user=UserMinimal(
                id=str(user.id),
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=user.role.value,
                organization_id=str(user.organization_id) if user.organization_id else None,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user and return JWT tokens"""
    try:
        user, access_token, refresh_token = await auth_service.login(data, db)

        await audit_service.log(
            db=db,
            action=AuditAction.USER_LOGIN,
            user_id=str(user.id),
            organization_id=str(user.organization_id) if user.organization_id else None,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=60 * 60,
            user=UserMinimal(
                id=str(user.id),
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=user.role.value,
                organization_id=str(user.organization_id) if user.organization_id else None,
            ),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token"""
    try:
        payload = auth_service.decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")
        from sqlalchemy import select
        from models.user import User
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        if not user.refresh_token_hash or not auth_service.verify_password(
            data.refresh_token, user.refresh_token_hash
        ):
            raise ValueError("Invalid refresh token")

        new_access_token = auth_service.create_access_token(
            str(user.id), user.role.value,
            str(user.organization_id) if user.organization_id else None,
        )
        new_refresh_token = auth_service.create_refresh_token(str(user.id))

        from sqlalchemy import update
        refresh_hash = auth_service.hash_password(new_refresh_token)
        await db.execute(
            update(User).where(User.id == user.id).values(refresh_token_hash=refresh_hash)
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=60 * 60,
            user=UserMinimal(
                id=str(user.id),
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=user.role.value,
                organization_id=str(user.organization_id) if user.organization_id else None,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Logout and invalidate refresh token"""
    from sqlalchemy import update
    await db.execute(
        update(User).where(User.id == current_user.id).values(refresh_token_hash=None)
    )

    await audit_service.log(
        db=db,
        action=AuditAction.USER_LOGOUT,
        user_id=str(current_user.id),
        ip_address=get_client_ip(request),
    )

    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user profile"""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role.value,
        "status": current_user.status.value,
        "organization_id": str(current_user.organization_id) if current_user.organization_id else None,
        "avatar_url": current_user.avatar_url,
        "is_mfa_enabled": current_user.is_mfa_enabled,
        "gdpr_consent": current_user.gdpr_consent,
        "last_login_at": current_user.last_login_at,
        "login_count": current_user.login_count,
        "created_at": current_user.created_at,
    }