import uuid
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict


def generate_slug(text: str, max_length: int = 100) -> str:
    import re
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    slug = slug.strip("-")
    return slug[:max_length]


def get_client_ip(request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def paginate(total: int, page: int, per_page: int) -> Dict[str, Any]:
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


def safe_str_uuid(val) -> str:
    if val is None:
        return ""
    return str(val)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)