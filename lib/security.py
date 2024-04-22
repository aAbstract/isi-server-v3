import os
import logging
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from lib.crypto import decode_jwt_token
from models.users import UserRole, AuthTokenClaims


LOGIN_ROUTE = f"{os.environ['API_ROOT']}/auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_ROUTE)


async def authorize_api(req: Request, access_token: str = Depends(oauth2_scheme)) -> AuthTokenClaims:
    role_path = req.url.path.split('/')[2]
    system_role = UserRole.map_route_role(role_path)
    if system_role == UserRole.GUEST:
        return None

    # validate authorization header
    try:
        # access_token = _parse_auth_token(x_auth)
        token_claims = decode_jwt_token(access_token)
        token_claims = AuthTokenClaims.model_validate(token_claims)
    except:
        err_msg = 'Unauthorized API Access [Invalid Token]'
        logging.getLogger('uvicorn').error(err_msg)
        raise HTTPException(status_code=403, detail=err_msg)

    # check user access
    role_code = system_role.value
    if role_code < token_claims.role.value:
        err_msg = 'Unauthorized API Access [Restricted Access]'
        logging.getLogger('uvicorn').error(err_msg)
        raise HTTPException(status_code=403, detail=err_msg)

    return token_claims
