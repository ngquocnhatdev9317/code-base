from typing import Generic, TypeVar

from core.base.view import BaseView

T = TypeVar("T")


class AdminAPIView(BaseView, Generic[T]):
    model: type[T]

    @property
    def get_service(self):
        return
