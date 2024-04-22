from fastapi import Request
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from models.runtime import Result
from fastapi.encoders import jsonable_encoder


class HttpOutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        try:
            result: Result = request.state.result
            if result.error:
                return JSONResponse(status_code=result.status_code, content={'detail': result.error})
            return JSONResponse(content=jsonable_encoder(result.success))

        except AttributeError:
            return response
