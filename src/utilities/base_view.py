from typing import Literal, Union

from aiohttp_pydantic import PydanticView
from pydantic import ValidationError

from utilities.middlewares.error_handle import get_validate_response

ContextType = Union[Literal["body"], Literal["headers"], Literal["path"], Literal["query string"]]


class BaseView(PydanticView):
    async def on_validation_error(self, exception: ValidationError, context: ContextType) -> None:
        errors = exception.errors(include_url=False)
        return get_validate_response(errors)
