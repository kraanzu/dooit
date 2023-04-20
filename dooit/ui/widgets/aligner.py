from typing import List
from rich.text import Text, TextType


def align_texts(items: List[TextType]):
    """
    Align the texts
    """

    def aligned(original: List[TextType]) -> List[Text]:
        """
        Align multiple items to same margin
        """

        texts: List[Text] = []
        for text in original:
            if not isinstance(text, Text):
                text = Text.from_markup(str(text))

            texts.append(text)

        max_len = max(len(i) for i in texts)
        for text in texts:
            text.pad_right(max_len - len(text))

        return texts

    formatted = []
    for text in items:
        if not isinstance(text, List):
            text = [text]

        formatted.extend(aligned(text))

    return formatted
