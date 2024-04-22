from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from enum import Enum


class UserRole(Enum):
    ADMIN = 0
    USER = 1
    GUEST = 2

    @classmethod
    def map_route_role(cls, role_path: str) -> 'UserRole':
        if role_path == 'admin':
            return cls.ADMIN
        elif role_path == 'user':
            return cls.USER
        else:
            return cls.GUEST


class User(BaseModel):
    id: str = None
    username: str
    disp_name: str
    pass_hash: str
    user_role: UserRole
    phone_number: str
    email: str
    is_online: bool = False

    model_config = ConfigDict(use_enum_values=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4())


class AuthTokenClaims(BaseModel):
    username: str
    display_name: str
    role: UserRole
