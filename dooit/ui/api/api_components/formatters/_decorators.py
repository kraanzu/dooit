def allow_multiple_formatting(func):
    """
    Decorator to allow multiple formatters to be registered for a single field.
    """

    func.__allow_multiple = True
    return func
