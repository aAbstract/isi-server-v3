from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.requests import Request
import database.users_database_api as users_database_api
from lib.security import LOGIN_ROUTE


router = APIRouter()


class AccessTokenResponse(BaseModel):
    access_token: str


@router.post(LOGIN_ROUTE)
async def login(req: Request, login_form: OAuth2PasswordRequestForm = Depends()) -> AccessTokenResponse | None:
    req.state.result = users_database_api.login_user(login_form.username, login_form.password)
