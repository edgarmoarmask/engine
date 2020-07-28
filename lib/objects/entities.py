import enum
from typing import List


class Span:
    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, value: int):
        self._start = value

    @property
    def end(self) -> int:
        return self._end

    @end.setter
    def end(self, value: int):
        self._end = value

    def __str__(self):
        return "[" + str(self.start) + "," + str(self.end) + "]"


class Token:
    def __init__(self, text: str):
        self.position: int = 0
        self.span: Span = Span(0,0)
        self.text: str = text
        self.lemma: str = ""

    # position
    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value

    # span
    @property
    def span(self) -> Span:
        return self._span

    @span.setter
    def span(self, value: Span):
        self._span = value

    # token
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def lemma(self) -> str:
        return self._lemma

    @lemma.setter
    def lemma(self, value: str):
        self._lemma = value

    def __str__(self):
        return self.text

class Tokens(List[Token]):

    def __init__(self):
        self._data = ""


    def text(self):
        return " ".join((self[i].text) for i in range(0, len(self)))

    @property
    def data(self)-> str:
        return self._data

    @data.setter
    def data(self, value: str):
        self._data = value

    def __str__(self):
        return " ".join(str(self[i]) for i in range(0, len(self)))

class EntityTypes(enum.Enum):
    PERSON =1
    ORGANIZATION = 2
    DATE = 3
    MONEY = 4
    CITY=5
    STATE_OR_PROVINCE = 6
    COUNTRY=7
    TITLE =8
    NUMBER = 9
    NATIONALITY=10
    LOCATION = 11
    DURATION = 12
    ORDINAL = 13
    PERCENT = 14
    TIME =15
    RELIGION = 16
    IDEOLOGY = 17

    CRIMINAL_CHARGE =30
    CAUSE_OF_DEATH = 31
    LAW = 32
    SET=33

    MISC = 100

    def to_string(self):
        val = str(self)
        vals = val.split(".")

        return vals[1]

class Entity():

    def __init__(self):
        self.tokens: Tokens = Tokens()

    @property
    def type(self) -> EntityTypes:
        return self._type

    @type.setter
    def type(self, type: EntityTypes):
        self._type = type

    @property
    def tokens(self)-> [Token]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: [Token]):
        self._tokens = value

    def text(self):
        return self.tokens.text()

    def span(self) -> Span:
        token_first: Token = self.tokens[0]
        token_last: Token = self.tokens[len(self.tokens) - 1]

        start_index = str(token_first.span.start)
        end_index = str(token_last.span.end)

        return Span(start_index, end_index)

    def __str__(self):

        span = self.span()

        return self.text() + ":" + self.type.to_string() + "-> [" + span.start + ":" + span.end + "]"

class Entities(List[Entity]):

    def __str__(self):
        return " , ".join(str(self[i].text()) for i in range(0, len(self)))

class Relation:
    def __init__(self):
        self.right: Tokens = Tokens()
        self.left: Tokens = Tokens()
        self.relation: str

    @property
    def right(self) -> Tokens:
        return self._right

    @right.setter
    def right(self, value: Tokens):
        self._right = value

    @property
    def left(self) -> Tokens:
        return self._left

    @left.setter
    def left(self, value: Tokens):
        self._left = value

    @property
    def relation(self)-> str:
        return self._relation

    @relation.setter
    def relation(self, value: str):
        self._relation = value

    def text(self):
        return "[{" + self.left.text + "},{" + self.right.text + "}-> " + str(self.relation) + "]"

    def __str__(self):
        left_text = str(self.left)
        if len(self.left.data) >0:
            left_text = left_text + "-" + self.left.data

        right_text = str(self.right)
        if len(self.right.data) > 0:
            right_text = right_text + "-" + self.right.data

        relation_text = str(self.relation)

        return "[{" + left_text + "},{" + right_text + "}-> " + relation_text + "]"


class Relations(List[Relation]):
    pass

class Sentence():

    def __init__(self):
        self.entities = Entities()
        self.relations = Relations()
        self.tokens = Tokens()

    @property
    def text(self) -> str:

        result = ""

        if len(self._text) > 0:
            return self._text
        else:
            tokens = self.tokens
            result = " ".join((tokens[i].text) for i in range(0, len(tokens)))

        return result

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def entities(self) -> Entities:
        return self._entities

    @entities.setter
    def entities(self, value: Entities):
        self._entities = value

    @property
    def relations(self) -> Relations:
        return self._relations

    @relations.setter
    def relations(self, value: Relations):
        self._relations = value

    @property
    def tokens(self) -> Tokens:
        return self._tokens

    @tokens.setter
    def tokens(self, value: Tokens):
        self._tokens = value

    def __str__(self):

        return str(self.entities)

class Sentences(List[Sentence]):
    pass



def get_entity_Barak():

    l1 = Token("Barak")
    l1.position = 1

    l2 = Token("Obama")
    l2.position = 2

    l3 = Token("Hussein")
    l3.position = 3

    result= Entity()
    result.tokens.append(l1)
    result.tokens.append(l2)
    result.tokens.append(l3)

    result.type = EntityTypes.PERSON

    return result

def get_entity_USA():
    l1 = Token("USA")
    l1.position = 5


    result= Entity()
    result.tokens.append(l1)

    result.type = EntityTypes.COUNTRY

    return result



def test_entities_object_mmodel():

    e = get_entity_Barak()

    print(e.text())
    print(e)


    test_sentences()

def test_sentences():

    s = Sentence("Barak Obama Hussein is the presdent of USA");

    s.entities.append(Info.get_entity_Barak_Obama_Hussein())
    s.entities.append(Info.get_entity_USA())

    s.tokens.extend(Info.get_entity_Barak_Obama_Hussein().tokens)
    s.tokens.extend(Info.get_entity_USA().tokens)

    rel = Info.get_relation_BarakToUSA()
    s.relations.append(rel)

    print(s)




class Info:

    @staticmethod
    def get_lemma_Barak():
        l = Token("Barak")
        l.position = 1
        return l

    @staticmethod
    def get_lemma_Obama():
        l = Token("Obama")
        l.position = 2
        return l

    @staticmethod
    def get_lemma_Hussein():
        l = Token("Hussein")
        l.position = 3
        return l

    @staticmethod
    def get_lemma_USA():
        l = Token("USA")
        l.position = 8
        return l


    @staticmethod
    def get_entity_Barak_Obama_Hussein():
        e = Entity()
        e.tokens.append(Info.get_lemma_Barak())
        e.tokens.append(Info.get_lemma_Obama())
        e.tokens.append(Info.get_lemma_Hussein())
        e.type = EntityTypes.PERSON
        return e

    @staticmethod
    def get_entity_USA():
        e = Entity()
        e.tokens.append(Info.get_lemma_USA())
        e.type = EntityTypes.COUNTRY
        return e

    @staticmethod
    def get_relation_BarakToUSA():
        left = Tokens()
        left.append(Info.get_lemma_Barak())
        left.append(Info.get_lemma_Hussein())
        left.append(Info.get_lemma_Hussein())

        right = Tokens()
        right.append(Info.get_lemma_USA())

        rel = Relation()
        rel.left = left
        rel.right = right
        rel.relation = "per:persident"

        return rel
