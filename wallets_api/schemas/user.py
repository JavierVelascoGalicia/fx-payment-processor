
from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class UserRequest(BaseModel):
    user_id: Optional[int] = None


class UserResponse(UserRequest, BaseModel):
    created_at: datetime
