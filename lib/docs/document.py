import spacy
from datetime import datetime


class Document():
    """A Class that Abstracts Document object, based on spacy library"""

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text

        self.nlp = spacy.load('en_core_web_sm')

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date: datetime):
        self.__date = date

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def sentences(self) -> [str]:
        doc = self.nlp(self.text)
        result = []
        for sent in doc.sents:
            result.append(sent.text)

        return result

    @classmethod
    def showMe(self):
        print("Title->", self.__title, "\n")
        print("Date->", self.__date, "\n")
        print("Text->", "\n", self.__text)
