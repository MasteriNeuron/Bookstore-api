# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db as _get_db
from .auth import get_current_active_user, get_current_admin
from .models import User


def get_db() -> Session:
    return next(_get_db())  # type: ignore[return-value]


# You can use these in routes if you want shorter names
CurrentUser = Depends(get_current_active_user)
CurrentAdmin = Depends(get_current_admin)
DBSession = Depends(_get_db)
