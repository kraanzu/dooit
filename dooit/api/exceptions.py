class DooitError(Exception):
    """
    Base class for all exceptions raised by the API.
    """


class SiblingAdditionError(DooitError):
    """
    Raised when user tries to add a sibling to a non-parented node (i.e Manager Object)
    """


class WorkspaceAdditionError(DooitError):
    """
    Raised when user tries to add a workspace to a todo object
    """


class TodoAdditionError(DooitError):
    """
    Raised when user tries to add a todo to manager class
    """
