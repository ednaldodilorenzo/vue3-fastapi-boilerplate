from fastapi import Query


class PaginatedParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=0),
        search: str = Query(""),
        paginate: bool = Query(True),
    ):
        self.page = page
        self.page_size = page_size
        self.search = search
        self.paginate = paginate
