from textual.message import Message


class ApiEvent(Message):
    """
    Base Class for all events that triggers an API call
    """

    event_name: str
