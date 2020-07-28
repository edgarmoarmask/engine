
import requests
import urllib.parse
import json

from lib.objects.entities import Sentence, Entity, Relation

opennre_server_url = "http://127.0.0.1:5124"


class OpenNREClient:
    def __init__(self, url):
        self.__url = url


    def extract(self, text: str, pos_h, pos_t) -> (str, float):

        url = self.__url
        clean_text = urllib.parse.quote(text)

        final_url = url + "/jmd?text=" + clean_text + "&h=" + pos_h + "&t=" + pos_t
        headers = {"Content-type": "application/json", "Accept": "text/json"}
        response = requests.post(final_url, headers=headers)

        result = {}

        try:
            result = json.loads(response.content)
        except SystemError:
            print("There is error in parsing -> ", response.content)

        return result

class OpenNreExtractor:
    def __init__(self):
        self.client: OpenNREClient = OpenNREClient(opennre_server_url)

    def extract(self, sentenceText: str,  sentence: Sentence) -> Sentence:

        result: Sentence =Sentence()
        result.entities.extend(sentence.entities)

        if len(sentence.entities) < 1:
            return result

        for i in range(0, len(result.entities) - 2):

            entity_first = result.entities[i]
            entity_second = result.entities[i + 1]

            r = self._extract_entities(sentenceText, entity_first, entity_second)

            relation_name = r[0]
            confidence = float(r[1])

            if (confidence > 0.8):
                rel: Relation = Relation()
                rel.left.extend(entity_first.tokens)
                rel.right.extend(entity_second.tokens)
                rel.relation = relation_name
                result.relations.append(rel)


        return result


    def _extract_entities(self, text, entity_h: Entity, entity_t: Entity):

        result = {"none", 0}

        if len(entity_h.tokens) == 0 or len(entity_t.tokens) ==0:
            return result

        entity_h_start_pos = entity_h.tokens[0].span.start
        entity_h_end_pos = entity_h.tokens[len(entity_h.tokens) - 1].span.end

        entity_t_start_pos = entity_t.tokens[0].span.start
        entity_t_end_pos = entity_t.tokens[len(entity_t.tokens) - 1].span.end

        pos_h = str(entity_h_start_pos) + "," + str(entity_h_end_pos)
        pos_t = str(entity_t_start_pos) + "," + str(entity_t_end_pos)

        result = self.client.extract(text, pos_h, pos_t)

        return result

    def _extract_plain(self, text, head, tail):
        result = {"none", 0}


        h = head.split(",")
        entity_h_start_pos = h[0]
        entity_h_end_pos = h[1]

        t = tail.split(",")
        entity_t_start_pos = t[0]
        entity_t_end_pos = t[1]

        pos_h = str(entity_h_start_pos) + "," + str(entity_h_end_pos)
        pos_t = str(entity_t_start_pos) + "," + str(entity_t_end_pos)

        result = self.client.extract(text, pos_h, pos_t)

        return result

