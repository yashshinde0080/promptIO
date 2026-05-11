import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.user import User, UserStatus, UserRole
from models.organization import Organization, PlanType
from schemas.auth import RegisterRequest, LoginRequest
from config import settings
import structlog

logger = structlog.get_logger(__name__)


class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    def hash_password(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')[:72]
        return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain.encode('utf-8')[:72], hashed.encode('utf-8'))
        except Exception:
            return False

    def hash_token(self, token: str) -> str:
        """Hash long tokens (like JWTs) with SHA256 pre-hash to fit bcrypt's 72-byte limit."""
        digest = hashlib.sha256(token.encode()).hexdigest()
        return bcrypt.hashpw(digest.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_token(self, token: str, hashed: str) -> bool:
        """Verify a token that was hashed with hash_token."""
        try:
            digest = hashlib.sha256(token.encode()).hexdigest()
            return bcrypt.checkpw(digest.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False

    def create_access_token(self, user_id: str, role: str, org_id: Optional[str] = None) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "role": role,
            "org_id": org_id,
            "type": "access",
            "iat": now,
            "exp": now + self.access_token_expire,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + self.refresh_token_expire,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    async def register(
        self, data: RegisterRequest, db: AsyncSession
    ) -> Tuple[User, Optional[Organization]]:
        # Check existing email
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Check existing username
        result = await db.execute(select(User).where(User.username == data.username))
        if result.scalar_one_or_none():
            raise ValueError("Username already taken")

        organization = None
        if data.organization_name:
            slug = data.organization_name.lower().replace(" ", "-")[:100]
            organization = Organization(
                name=data.organization_name,
                slug=f"{slug}-{str(uuid.uuid4())[:8]}",
                plan=PlanType.FREE,
            )
            db.add(organization)
            await db.flush()

        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            password_hash=self.hash_password(data.password),
            role=UserRole.ADMIN if data.organization_name else UserRole.PROMPT_ENGINEER,
            organization_id=organization.id if organization else None,
            gdpr_consent=data.gdpr_consent,
            gdpr_consent_at=datetime.now(timezone.utc) if data.gdpr_consent else None,
            status=UserStatus.ACTIVE,
        )

        db.add(user)
        await db.flush()

        logger.info("User registered", user_id=str(user.id), email=user.email)
        return user, organization

    async def login(
        self, data: LoginRequest, db: AsyncSession
    ) -> Tuple[User, str, str]:
        result = await db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()

        if not user or not self.verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        if user.status == UserStatus.SUSPENDED:
            raise ValueError("Account suspended. Contact support.")

        if user.status == UserStatus.INACTIVE:
            raise ValueError("Account inactive. Please verify your email.")

        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise ValueError(f"Account locked until {user.locked_until}")

        # Update login tracking
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                last_login_at=datetime.now(timezone.utc),
                login_count=User.login_count + 1,
                failed_login_attempts=0,
            )
        )

        access_token = self.create_access_token(
            str(user.id), user.role.value, str(user.organization_id) if user.organization_id else None
        )
        refresh_token = self.create_refresh_token(str(user.id))

        refresh_hash = self.hash_token(refresh_token)
        await db.execute(
            update(User).where(User.id == user.id).values(refresh_token_hash=refresh_hash)
        )

        logger.info("User logged in", user_id=str(user.id))
        return user, access_token, refresh_token

    async def get_current_user(self, token: str, db: AsyncSession) -> User:
        payload = self.decode_token(token)

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        if user.status != UserStatus.ACTIVE:
            raise ValueError("User account is not active")

        return user


auth_service = AuthService()