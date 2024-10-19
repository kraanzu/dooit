MUTLIPLE_FORMATTER_ATTR = "__allow_multiple"

def allow_multiple_formatting(func):
    """
    Decorator to allow multiple formatters to be registered for a single field.
    """

    setattr(func, MUTLIPLE_FORMATTER_ATTR, True)
    return func
