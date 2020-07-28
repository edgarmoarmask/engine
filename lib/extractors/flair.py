from flair.data import Sentence
from flair.models import SequenceTagger

from lib.objects.entities import Tokens, Token, Span, Entity, EntityTypes


from lib.objects.entities import Sentence as Sent

class FlairExtractor:

    def __init__(self, modelName="ner-ontonotes"):
        self.tagger: SequenceTagger = SequenceTagger.load(modelName)

    def extract(self, text) -> Sent:

        result = Sent(text)
        sentence = Sentence(text)

        self.tagger.predict(sentence)

        ners = sentence.get_spans('ner')
        tokens = sentence.tokens

        tokens = Tokens()

        for t in tokens:
            tokens.append(self._get_token(t))


        result.tokens.extend(tokens)

        for e in ners:
            ent = Entity()

            for t in e.tokens:
                ent.tokens.append(self._get_token(t))

            ent.type = Coverter.convert_to_corenlp_entity_type(e.tag)
            result.entities.append(ent)

        return result

    def _get_token(self, token):

        result = Token(token.text)
        result.span = Span(token.start_position, token.end_position)
        result.position = token.idx

        return result

class Coverter():

    @staticmethod
    def convert_to_corenlp_entity_type(flair_entity):
        result: EntityTypes = EntityTypes.MISC

        if (flair_entity == "ORG"):
            result = EntityTypes.ORGANIZATION
        elif (flair_entity == "PERSON"):
            result = EntityTypes.PERSON
        elif (flair_entity == "LAW"):
            result = EntityTypes.LAW
        elif (flair_entity == "DATE"):
            result = EntityTypes.DATE
        elif (flair_entity == "MONEY"):
            result = EntityTypes.MONEY
        elif flair_entity == "CARDINAL":
            result = EntityTypes.NUMBER
        return result
