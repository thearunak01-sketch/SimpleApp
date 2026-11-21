def pagination_response(pagination, serialize):
    return {
        "items": [serialize(item) for item in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_records": pagination.total,
        "total_pages": pagination.pages or 1,
        "has_next": pagination.has_next,
        "has_previous": pagination.has_prev,
    }


def parse_pagination_args(request, default_per_page=10, max_per_page=50):
    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(max(1, int(request.args.get("per_page", default_per_page))), max_per_page)
    except ValueError as error:
        raise ValueError("page and per_page must be positive numbers") from error
    return page, per_page
