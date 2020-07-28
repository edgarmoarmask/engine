from typing import List

from lib.objects.entities import Span


class CorefItem:
    def __init__(self):
        self.span = Span(0, 0)
        self.is_main = False


    @property
    def span(self) -> Span:
        return self._span

    @span.setter
    def span(self, value: Span):
        self._span = value

    @property
    def is_main(self) -> bool:
        return self._ismain

    @is_main.setter
    def is_main(self, value: bool):
        self._ismain = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def sentNumber(self) -> int:
        return self._sentNum

    @sentNumber.setter
    def sentNumber(self, value: int):
        self._sentNum = value


class CorefCluster(List[CorefItem]):
    def __init__(self):
        pass

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value


    def is_coreferenced(self, text, sentenceNumber = -1, is_include_main = False):
        result = None
        others_coref = self._get_others()

        if (is_include_main == True):
            others_coref.append(self._get_main())

        for item in others_coref:
            item_text: str = item.text

            if (item_text == text):
                if (sentenceNumber > 0):
                    if item.sentNumber == sentenceNumber:
                        result = self._get_main()
                else:
                    result = self._get_main()

        return result

    def _get_main(self) -> CorefItem:

        result = CorefItem()
        for item in self:
            if (item.is_main == True):
                result = item
        return result

    def _get_others(self) -> list:
        result = list()
        for item in self:
            if (item.is_main == False):
                result.append(item)

        return result

    def __str__(self):

        others_coref = self._get_others()
        main_coref = self._get_main()


        result = main_coref.text

        others_coref_text = " , ".join(item.text for item in others_coref)

        result = result + " -> " + others_coref_text

        return result




class CorefClusters(List[CorefCluster]):

    def is_coreferenced(self, text, sentenceNumber = -1, is_include_main = False):
        result: CorefItem = None

        for item in self:
            result = item.is_coreferenced(text, sentenceNumber=sentenceNumber, is_include_main=is_include_main)
            if (result != None):
                break

        return result

