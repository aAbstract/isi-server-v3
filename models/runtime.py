from typing import Optional, Any
from pydantic import BaseModel


class Result(BaseModel):
    status_code: int = 200
    success: Optional[Any] = None
    error: Optional[str] = None
