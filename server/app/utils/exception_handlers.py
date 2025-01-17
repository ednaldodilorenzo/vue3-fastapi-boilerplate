import sys
from app.utils.exception import BusinessException, CredentialsException
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    # logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    if exception_type is KeyError:
        return PlainTextResponse(str(exc), status_code=404)
    # logger.error(
    #     f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    # )
    return PlainTextResponse(str(exc), status_code=500)


async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = [{"field": err["loc"][0], "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Validation Error", "details": errors},
    )


async def validation_credentials_exception(request: Request, exc: CredentialsException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)})


async def validation_business_exception(request: Request, exc: BusinessException):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": str(exc)})


async def validation_request_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    modified_details = []
    # Replace 'msg' with 'message' for each error
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"][0],
                "field": error["loc"][1],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": modified_details}),
    )
