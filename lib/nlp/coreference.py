


"""

model_url = "https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz"

text = "Barak Obama is the president of USA. He has beautiful wife Michelle Obama and daughter Natasha Obama. He also has served as senator from Illinois."


predictor = Predictor.from_path(model_url)

result = predictor.coref_resolved(document=text)

print(result)


"""

from allennlp.predictors.predictor import Predictor

from lib.objects.corefs import CorefClusters
from lib.objects.doc import Document
from lib.objects.entities import Relations, Tokens, Relation, Entity


class Coreference:
    def __init__(self):
        model_url = "https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz"
        self.predictor = Predictor.from_path(model_url)

    def resolve(self, text):
        result = self.predictor.coref_resolved(document=text)
        return result


    @staticmethod
    def resolve_coref( relations: Relations, doc: Document, sentence_number):

        result = Relations()

        for rel in relations:
            
            r = Relation()
            r.relation = rel.relation

            left_entity: Entity = Coreference.find_tokens_entity(rel.left, doc, sentence_number)
            right_entity : Entity = Coreference.find_tokens_entity(rel.right, doc, sentence_number)

            if left_entity!=None and right_entity!=None:

                r.left = left_entity.tokens
                r.left.data = rel.left.text()
                r.right = right_entity.tokens
                r.right.data = rel.right.text()
                result.append(r)


        return result
    
    @staticmethod
    def find_tokens_entity(relation: Tokens, doc: Document, sentence_number)-> Entity:
        
        result: Entity = None
        text = relation.text()
        coref = doc.coref_clusters.is_coreferenced(text, sentenceNumber=sentence_number)

        this_sentence = None
        try:
            this_sentence = doc.sentences[sentence_number]
        except Exception:
            print(sentence_number)


        if (coref != None):
            this_sentence = doc.sentences[coref.sentNumber -1]
            tks_list = this_sentence.tokens[coref.span.start - 1: coref.span.end - 1]
            tks: Tokens = Tokens()
            tks.extend(tks_list)
            text = tks.text()
        
        for e in this_sentence.entities:
            entity_text = e.text()
            if text.find(entity_text) != -1:
                result = e
                break
        
        return result
    