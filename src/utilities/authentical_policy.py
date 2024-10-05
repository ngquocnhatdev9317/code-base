from functools import wraps

from aiohttp.web_exceptions import HTTPUnauthorized

from authentication.service import AuthenticationService
from utilities.constants import AUTH_KEY


async def authentication_handle(request):
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPUnauthorized(reason="Missing authorization header")

    if authorization.split(" ")[0] != "Bearer":
        raise HTTPUnauthorized(reason="Invalid token scheme")

    access_token = authorization.split(" ")[1]
    service = AuthenticationService(request)
    user = await service.verify_access(access_token)

    if not user:
        raise HTTPUnauthorized(reason="Invalid access token")

    return user


def authentication_wrapper(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        user = await authentication_handle(self.request)
        self.request.app[AUTH_KEY] = user
        return await func(self, *args, **kwargs)

    return wrapper


def authentication_class_wrapper(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and attr_name in ("get", "post", "put", "patch", "delete"):
            wrapper = wraps(attr_value)(authentication_wrapper(attr_value))
            wrapper.__doc__ = f"""
                {wrapper.__doc__}
        Security: bearerAuth
        """
            setattr(cls, attr_name, wrapper)

    return cls
