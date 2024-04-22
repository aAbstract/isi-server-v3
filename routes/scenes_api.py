import os
from fastapi import APIRouter, Depends, Body
from fastapi.requests import Request
from lib.security import authorize_api
from models.users import AuthTokenClaims
import database.scenes_database_api as scenes_database_api
from models.iot import Scene


# _ADMIN_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/admin/scenes"
_USER_ROOT_ROUTE = f"{os.getenv('API_ROOT')}/user/scenes"
router = APIRouter()


@router.post(f"{_USER_ROOT_ROUTE}/get-scenes-metadata")
async def get_scenes_metadata(req: Request, _: AuthTokenClaims = Depends(authorize_api)) -> list[Scene] | None:
    req.state.result = scenes_database_api.get_scenes_metadata()


@router.post(f"{_USER_ROOT_ROUTE}/get-scene")
async def get_scene(req: Request, scene_id: str = Body(embed=True), _: AuthTokenClaims = Depends(authorize_api)) -> Scene | None:
    req.state.result = scenes_database_api.get_scene(scene_id)
