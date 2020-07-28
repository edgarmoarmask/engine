


class StringUtils():

    @staticmethod
    def InsertInto(text: str, insertText: str, insertAtPosition:int) -> str:
        text_chars = list(text)
        text_chars.insert(insertAtPosition, insertText)
        result = ''.join(text_chars)

        return result