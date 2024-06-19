from typing import Generic, Optional, TypeVar

from aiohttp import web

T = TypeVar("T")


class BaseService(Generic[T]):
    repository_class: type[T]

    def __init__(self, request: Optional[web.Request] = None) -> None:
        self._request = request

    @property
    def request(self) -> web.Request | None:
        return self._request

    @property
    def repository(self) -> T:
        if self.request:
            return self.repository_class(self.request)

        raise ValueError("No request provided")
