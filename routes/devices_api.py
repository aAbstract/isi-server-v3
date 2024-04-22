import os
from fastapi import APIRouter, Depends, Body
from fastapi.requests import Request
from lib.security import authorize_api
from models.users import AuthTokenClaims
import database.devices_database_api as devices_database_api
from models.iot import Device


# _ADMIN_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/admin/devices"
_USER_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/user/devices"
router = APIRouter()


@router.post(f"{_USER_ROOT_ROUTE}/get-room-devices")
async def get_room_devices(req: Request, room_name: str = Body(embed=True), _: AuthTokenClaims = Depends(authorize_api)) -> list[Device] | None:
    req.state.result = devices_database_api.get_room_devices(room_name)


@router.post(f"{_USER_ROOT_ROUTE}/get-device")
async def get_device(req: Request, device_name: str = Body(embed=True), _: AuthTokenClaims = Depends(authorize_api)) -> list[Device] | None:
    req.state.result = devices_database_api.get_device(device_name)


@router.post(f"{_USER_ROOT_ROUTE}/get-temp-humd-devices")
async def get_temp_humd_device(req: Request, _: AuthTokenClaims = Depends(authorize_api)) -> list[Device] | None:
    req.state.result = devices_database_api.get_temp_humd_devices()
