from lib.objects.entities import Sentence, Entities, Tokens, Token, Span, Entity, EntityTypes, Relations, \
    Relation, Sentences
from stanfordcorenlp import StanfordCoreNLP
import json

from lib.objects.corefs import CorefClusters, CorefCluster, CorefItem
from lib.objects.doc import Document

server_url = "http://127.0.0.1"
port = 23456


class CoreNlpClient:
    def __init__(self, server, port):
        self.client = StanfordCoreNLP(server, port=port)

    def getResponse(self, text, annotators='ner, dcoref, relation, openie, kbp'):
        props = {'annotators': annotators, 'pipelineLanguage': 'en', 'outputFormat': 'json'}
        result = self.client.annotate(text, properties=props)
        result = json.loads(result)

        return result


class CoreNlpExtractor:

    def __init__(self):
        self.client: CoreNlpClient = CoreNlpClient(server_url, port)

    def extract_corefs(self, documentText: str) -> Document:

        annotations = 'dcoref'

        result: Document = Document(documentText)
        res = None

        try:
            res = self.client.getResponse(text=documentText, annotators=annotations)
        except Exception:
            print(Exception)

        if (res == None):
            return result

        res_corefs = res["corefs"]

        corefs = self._extract_coref(res_corefs)
        result.coref_clusters = corefs

        return result

    def extract_document(self, documentText) -> Document:
        annotations = 'ner, dcoref, relation, openie, kbp'

        result: Document = Document(documentText)
        res = None

        try:
            res = self.client.getResponse(text=documentText, annotators=annotations)
        except Exception:
            print(Exception)

        if (res == None):
            return result

        res_sentences = res["sentences"]
        res_corefs = res["corefs"]

        sents = self._extract_sentences(res_sentences)
        corefs = self._extract_coref(res_corefs)

        result.sentences = sents
        result.coref_clusters = corefs

        return result

    def extract(self, text) -> Sentence:
        annotations = 'ner, dcoref, relation, openie, kbp'
        res = self.client.getResponse(text=text, annotators=annotations)

        res_sentences = res["sentences"]

        result: Sentence = Sentence()

        for s in res_sentences:
            sent = Sentence()

            tks = s["tokens"]
            openie = s["openie"]
            kbs = s["kbp"]
            e = s["entitymentions"]

            if len(tks) > 0:
                sent.tokens.extend(self._extract_tokens(tks))

            if len(e) > 0:
                sent.entities.extend(self._extract_entities(e, sent.tokens))

            if len(kbs) > 0:
                sent.relations.extend(self._extract_kbrelations(kbs, sent.tokens))

            result = sent

        return result

    def _extract_coref(self, corefs_json):

        result: CorefClusters = CorefClusters()

        for cf_index in corefs_json:
            coref = CorefCluster()

            for cf_item in corefs_json[cf_index]:
                coref_item = CorefItem()

                startIndex = int(cf_item["startIndex"])
                endIndex = int(cf_item["endIndex"])

                coref_item.text = cf_item["text"]
                coref_item.type = cf_item["type"]
                coref_item.sentNumber = cf_item["sentNum"]
                coref_item.is_main = bool(cf_item["isRepresentativeMention"])
                coref_item.span = Span(startIndex, endIndex)
                coref.append(coref_item)

            result.append(coref)

        return result

    def _extract_sentences(self, sentece_json) -> Sentences:

        result: Sentences = Sentences()

        for s in sentece_json:
            sent = Sentence()

            tks = s["tokens"]
            openie = s["openie"]
            kbs = s["kbp"]
            e = s["entitymentions"]

            if len(tks) > 0:
                sent.tokens.extend(self._extract_tokens(tks))

            if len(e) > 0:
                sent.entities.extend(self._extract_entities(e, sent.tokens))

            if len(kbs) > 0:
                sent.relations.extend(self._extract_kbrelations(kbs, sent.tokens))

            result.append(sent)

        return result

    def _extract_tokens(self, t_json):
        result: Tokens = Tokens()

        for t in t_json:
            idx = t["index"]
            span_start = t["characterOffsetBegin"]
            span_end = t["characterOffsetEnd"]
            text = t["originalText"]
            lemma = t["lemma"]

            token: Token = Token(text)
            token.span = Span(int(span_start), int(span_end))
            token.position = int(idx)
            token.lemma = lemma

            result.append(token)

        return result

    def _extract_entities(self, e_json, tokens: Tokens) -> Entities:

        result: Entities = Entities()

        for e in e_json:
            token_begin = int(e["tokenBegin"])
            token_end = int(e["tokenEnd"])
            type = e["ner"]

            tks = tokens[token_begin: token_end]

            entity = Entity()
            entity.tokens.extend(tks)
            entity.type = Converter.convert_to_corenlp_entity_type(type)

            result.append(entity)

        return result

    def _extract_kbrelations(self, kb_json, tokens: Tokens):
        result: Relations = Relations()

        for kb in kb_json:
            sub_span = kb["subjectSpan"]
            obj_span = kb["objectSpan"]
            rel_desc = kb["relation"]

            rel: Relation = Relation()
            rel.relation = rel_desc

            rel.left.extend(tokens[int(sub_span[0]): int(sub_span[1])])
            rel.right.extend(tokens[int(obj_span[0]): int(obj_span[1])])
            result.append(rel)

        return result


class Converter:

    @staticmethod
    def convert_to_corenlp_entity_type(entity_type):
        result: EntityTypes = EntityTypes.MISC

        if entity_type == "ORGANIZATION":
            result = EntityTypes.ORGANIZATION
        elif entity_type == "PERSON":
            result = EntityTypes.PERSON
        elif entity_type == "TITLE":
            result = EntityTypes.TITLE
        elif entity_type == "DATE":
            result = EntityTypes.DATE
        elif entity_type == "MONEY":
            result = EntityTypes.MONEY
        elif entity_type == "NUMBER":
            result = EntityTypes.NUMBER
        elif entity_type == "CITY":
            result = EntityTypes.CITY
        elif entity_type == "CRIMINAL_CHARGE":
            result = EntityTypes.CRIMINAL_CHARGE
        elif entity_type == "CAUSE_OF_DEATH":
            result = EntityTypes.CAUSE_OF_DEATH
        elif entity_type == "NATIONALITY":
            result = EntityTypes.NATIONALITY
        elif entity_type == "COUNTRY":
            result = EntityTypes.COUNTRY
        elif entity_type == "LOCATION":
            result = EntityTypes.LOCATION
        elif entity_type == "DURATION":
            result = EntityTypes.DURATION
        elif entity_type == "ORDINAL":
            result = EntityTypes.ORDINAL
        elif entity_type == "PERCENT":
            result = EntityTypes.PERCENT
        elif entity_type == "STATE_OR_PROVINCE":
            result = EntityTypes.STATE_OR_PROVINCE
        elif entity_type == "TIME":
            result = EntityTypes.TIME
        elif entity_type == "RELIGION":
            result = EntityTypes.RELIGION
        elif entity_type == "IDEOLOGY":
            result = EntityTypes.IDEOLOGY
        elif entity_type == "SET":
            result = EntityTypes.SET

        return result

    @staticmethod
    def convert_to_simplified_relation_name(renation_name) -> str:

        relation_alternative_names = {
            # work
            "per:employee_or_member_of": "work",
            "org:top_members_employees": "manage",

            # org details
            "org:founded_by": "founded",
            "org:country_of_headquarters": "headquarter",
            "org:city_of_headquarters": "headquarter",
            "org:subsidiaries": "part_of",

            # person residence
            "per:countries_of_residence": "residence",
            "per:cities_of_residence": "residence",
            "per:statesorprovinces_of_residence": "residence",

            # person details
            "per:origin": "origin",
            "per:religion": "religion",

            # person family
            "per:other_family": "family",
            "per:siblings": "sibling",
            "org:parents": "parents",
            "per:spouse": "spouse",
            "per:children": "children",

            # person death
            "per:city_of_death": "city_of_death",
            "per:date_of_death": "date_of_death",

            # person birth
            "per:city_of_birth": "city_of_birth",
            "per:country_of_birth": "country_of_birth"

        }

        result = relation_alternative_names.get(renation_name, renation_name)

        return result

