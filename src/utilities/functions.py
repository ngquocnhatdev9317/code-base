import os
from http import HTTPStatus
from typing import Any, List, Optional, get_origin, get_type_hints

_LIST_STATUS = [f"r{status}" for status in range(100, 500 + 1)]


def get_path(path: str) -> str:
    full_path = os.path.join(os.getcwd(), ".", path)

    if os.path.exists(full_path):
        return full_path

    return os.path.join(os.getcwd(), "..", path)


def get_status_description(status: int, description: Optional[str]) -> Optional[str]:
    if description:
        return description
    try:
        return HTTPStatus(status).phrase
    except ValueError:
        return None


def get_status_from_response_type(response_type: Any) -> Optional[int]:
    return int(get_origin(response_type).__name__.replace("r", ""))


def get_return_type_as_list(func) -> List[int]:
    hints = get_type_hints(func)
    return_type = hints.get("return")

    list_status = []

    if hasattr(return_type, "__args__") and get_origin(return_type).__name__ == "Union":
        list_status = [get_status_from_response_type(arg) for arg in return_type.__args__]

    elif hasattr(return_type, "__args__") and get_origin(return_type).__name__ in _LIST_STATUS:
        list_status = [get_status_from_response_type(return_type)]

    elif return_type.__name__ in _LIST_STATUS:
        list_status = [int(return_type.__name__.replace("r", ""))]

    return sorted(list_status)
