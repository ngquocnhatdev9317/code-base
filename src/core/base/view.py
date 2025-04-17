from functools import wraps
from typing import Dict, Literal, Optional, Union

from aiohttp_pydantic import PydanticView
from pydantic import ValidationError

from core.authentical import authentication_wrapper
from core.middlewares.error_handle import get_validate_response
from utilities.functions import get_return_type_as_list, get_status_description

ContextType = Union[Literal["body"], Literal["headers"], Literal["path"], Literal["query string"]]


class BaseView(PydanticView):
    async def on_validation_error(self, exception: ValidationError, context: ContextType) -> None:
        errors = exception.errors(include_url=False)
        return get_validate_response(errors)


_API_DOCSTRING_WITH_AUTH = """
        %s

        Tags: %s

        Security: %s

        Status Codes:%s
"""

_API_DOCSTRING_WITHOUT_AUTH = """
        %s

        Tags: %s

        Status Codes:%s
"""

_STATUS_CODES = """
            %i: %s"""


def api_docs(
    tag: Optional[str] = None,
    description: Optional[str] = None,
    authenticator: bool = False,
    response: Optional[Dict[int, str]] = None,
):
    """
    A decorator function to add API documentation to a view function.

    Parameters:
    - tag (Optional[str]): The tag for the API documentation. Defaults to None.
    - description (Optional[str]): The description of the API. Defaults to None.
    - authenticator (bool): A flag indicating whether authentication is required. Defaults to False.
        Note: authenticator = True will add logic verify authentication.
    - response (Optional[Dict[int, str]]): A dictionary mapping status codes to their descriptions. Defaults to None.

    Returns:
    - decorator: A decorator function that adds API documentation to the view function.
    """

    def decorator(func):
        _response = response or {200: "API Success"}
        _description = description or func.__doc__.strip() or f"API {func.__name__}"
        _tag = tag or "Common"

        res_list = get_return_type_as_list(func) or [200]

        status_code = ""

        for res in res_list:
            status_code += _STATUS_CODES % (res, get_status_description(res, _response.get(res)))

        docstring = _API_DOCSTRING_WITHOUT_AUTH % (_description, _tag, status_code)
        if authenticator:
            docstring = _API_DOCSTRING_WITH_AUTH % (_description, _tag, "bearerAuth", status_code)

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            return await func(self, *args, **kwargs)

        wrapper.__doc__ = docstring

        if authenticator:
            return wraps(wrapper)(authentication_wrapper(wrapper))

        return wrapper

    return decorator
