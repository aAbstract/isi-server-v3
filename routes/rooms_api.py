import os
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from lib.security import authorize_api
from models.users import AuthTokenClaims
import database.rooms_database_api as rooms_database_api
from models.iot import Room


# _ADMIN_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/admin/rooms"
_USER_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/user/rooms"
router = APIRouter()


@router.post(f"{_USER_ROOT_ROUTE}/get-rooms")
async def get_rooms(req: Request, _: AuthTokenClaims = Depends(authorize_api)) -> list[Room] | None:
    req.state.result = rooms_database_api.get_rooms()
