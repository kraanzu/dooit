from dooit.utils import Topic


class WorkSpace:
    """
    WorkSpace Manager
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.topics: dict[str, Topic] = dict()
        self.topics["common"] = Topic("common")

    def remove_topic(self, topic: str) -> None:
        del self.topics[topic]

    def add_topic(self, topic: str) -> None:
        self.topics[topic] = Topic(topic)

    def rename_topic(self, topic: str, name) -> None:
        self.topics[name] = self.topics[topic]
        self.topics[name].rename(name)
        self.remove_topic(topic)
