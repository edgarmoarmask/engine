
from lib.objects.corefs import  CorefClusters
from lib.objects.entities import Sentences, Entities


class Document():

    def __init__(self, text):
        self.text = text
        self.sentences = Sentences()
        self.coref_clusters = CorefClusters()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def sentences(self) -> Sentences:
        return self._sents

    @sentences.setter
    def sentences(self, value: Sentences):
        self._sents = value

    @property
    def coref_clusters(self) -> CorefClusters:
        return self._coref_clusters

    @coref_clusters.setter
    def coref_clusters(self, value: CorefClusters):
        self._coref_clusters = value

    def all_entities(self):
        result: Entities = Entities()

        for s in self.sentences:
            if len(s.entities) > 0:
                result.extend(s.entities)

        return result
