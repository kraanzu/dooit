MUTLIPLE_FORMATTER_ATTR = "__extra_formatter"


def extra_formatter(func):
    """
    Decorator to allow multiple formatters to be registered for a single field.
    """

    setattr(func, MUTLIPLE_FORMATTER_ATTR, True)
    return func
