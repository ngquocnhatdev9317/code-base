from functools import wraps

from aiohttp.web_exceptions import HTTPUnauthorized

from authentication.service import AuthenticationService


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
        self.request["user"] = user
        return await func(self, *args, **kwargs)

    return wrapper
