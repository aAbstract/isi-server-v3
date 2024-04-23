import os
from fastapi import APIRouter, Depends, Body
from fastapi.requests import Request
from lib.security import authorize_api
from models.users import AuthTokenClaims
import database.devices_database_api as devices_database_api
from models.iot import Device, DeviceConfig


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


@router.post(f"{_USER_ROOT_ROUTE}/change-device-config")
async def change_device_config(req: Request, device_name: str = Body(), config_name: str = Body(), config_new_val: bool = Body(), _: AuthTokenClaims = Depends(authorize_api)) -> DeviceConfig | None:
    req.state.result = devices_database_api.change_device_config(device_name, config_name, config_new_val)
