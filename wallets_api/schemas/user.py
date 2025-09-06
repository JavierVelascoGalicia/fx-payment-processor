
from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class UserRequest(BaseModel):
    user_id: Optional[int] = None


class UserResponse(UserRequest):
    created_at: datetime
