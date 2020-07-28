
from storage.db import Db
from lib.docs.newsDocument import NewsDocument
from lib.extractors.corenlp import CoreNlpExtractor, Converter
from lib.extractors.hmtl import HmtlExtractor
from lib.extractors.opennre import OpenNreExtractor
from lib.objects.entities import Entities, Relations, Relation
from storage.entity_urls import EntityUrls


file_type = "txt"

corenlp_extractor = CoreNlpExtractor()
opennre_extractor = OpenNreExtractor()
hmtl_extractor = HmtlExtractor()


class Crawler:
    def __init__(self, db_name, doc_files: list):
        self._db: Db = Db(db_name=db_name)
        self._doc_files = doc_files
        self._doc_dates = {}

    @property
    def db(self) -> Db:
        return self._db

    @property
    def doc_files(self) -> list:
        return self._doc_files

    def crawl(self):

        for f in self.doc_files:

            doc = NewsDocument.Load(f)

            doc_id = self.db.documents.add_record(doc.title, f, doc.date, doc.text)
            doc_sentences = corenlp_extractor.extract_document(doc.text)


            self._doc_dates[doc_id] = doc.date

            for sent in doc_sentences.sentences:
                sent_text = sent.tokens.text()

                self._crawl_entity_details(doc_id, sent.entities)
                self._crawl_relation_details(doc_id, sent.relations)

                hmtl_sent = hmtl_extractor.extract(sent_text)
                self._crawl_relation_details( doc_id, hmtl_sent.relations)

                opennre_sent = opennre_extractor.extract(sent_text, sent)
                self._crawl_relation_details(doc_id, opennre_sent.relations)

        self.db.save()

    def _crawl_entity_details(self, doc_id: int, entities: Entities):
        for e in entities:
            entity_name = e.text()
            entity_type = e.type.to_string()
            entity_type_enum = e.type
            entity_span = e.span()

            # ENTITY_TYPES
            entity_type_id = 0
            is_type_found = self.db.entity_types.find_by_name(entity_type)
            if (len(is_type_found) == 0):
                entity_type_id = self.db.entity_types.add_record(entity_type, entity_type)
            else:
                entity_type_id = is_type_found[0].id

            # ENTITIES
            (id, name, type_id) = self._find_entity_by_name(entity_name)
            if (id == -1):
                entity_url = EntityUrls.get_url(entity_type_enum)
                id = self.db.entities.add_record(name=entity_name, type=entity_type_id, image=entity_url)
            else:
                type_id = entity_type_id
            # print(str(e), " ->", entity_id)

            # ENTITY_MENTIONS
            self.db.entity_mentions.add_record(id, doc_id, entity_span.start, entity_span.end, self._doc_dates[doc_id])

    def _find_entity_by_name(self, entity_name) -> (int, str, int):
        entity_id = -1
        entity_type_id = -1
        is_entity_found = self.db.entities.find_by_name(entity_name)
        if (len(is_entity_found) > 0):
            entity_id = is_entity_found[0].id
            entity_name = is_entity_found[0].name
            entity_type_id = is_entity_found[0].type

        return (entity_id, entity_name, entity_type_id)

    def _crawl_relation_details(self, doc_id, relations: Relations):

        for r in relations:

            r_name = Converter.convert_to_simplified_relation_name(r.relation)

            """
            if (r_name in self.get_entity_attribute_types()):
                self._crawl_attribute_details(doc_id, r)
                continue


            if (r_name in self.get_alternative_names()):
                self._crawl_alternate_names(doc_id, r)
                continue
            """

            (left_entity_id, left_entity_name, left_entity_type_id) = self._find_entity_by_name(r.left.text())
            (right_entity_id, right_entity_name, right_entity_type_id) = self._find_entity_by_name(r.right.text())

            if (left_entity_id != -1 and right_entity_id != -1):

                event_id = -1
                event_found = self.db.event_types.find_by_name(r_name)
                if (len(event_found) > 0):
                    event_id = event_found[0].id
                else:
                    event_id = self.db.event_types.add_record(r_name, r_name)

                self.db.event_mentions.add_record(event_id, doc_id, left_entity_id, right_entity_id, self._doc_dates[doc_id])

                left = left_entity_name + " : " + str(left_entity_id) + " : " + \
                       self.db.entity_types.find_by_id(left_entity_type_id)[0].name
                right = right_entity_name + " : " + str(right_entity_id) + " : " + \
                        self.db.entity_types.find_by_id(right_entity_type_id)[0].name
                print("[", left, " , ", right, "]", "->", r_name)

    def get_entity_attribute_types(self):
        result = [
            "per:title",
            "per:age",
            "per:charges"
        ]
        return result

    def get_alternative_names(self):
        result = ["org:alternate_names"]
        return result

    def _crawl_attribute_details(self, doc_id, relation: Relation):
        pass
        print("attribute ==>", relation)

    def _crawl_alternate_names(self, doc_id, relation: Relation):


        print("alternative_names ==>", relation)

