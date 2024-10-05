from aiohttp_pydantic.injectors import Group


class PaginationRequest(Group):
    page: int = 1
    page_size: int = 30
