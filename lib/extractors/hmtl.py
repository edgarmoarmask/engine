
import requests
import urllib.parse
import json

from lib.objects.entities import Relations, Relation, Sentence, Tokens, Token

server= 'http://localhost'
port=5123


class HmtlClient:
    def __init__(self, url):
        self.__url = url


    def extract(self, text: str):

        url = self.__url
        clean_text = urllib.parse.quote(text)

        final_url = url + "/jmd?text=" + clean_text
        headers = {"Content-type": "application/json", "Accept": "text/json"}
        response = requests.post(final_url, headers=headers)

        result = {}

        try:
            result = json.loads(response.content)
        except SystemError:
            print("There is error in parsing -> ", response.content)

        return result

class HmtlExtractor:
    def __init__(self):
        url = server + ":" + str(port)
        self.client = HmtlClient(url)


    def extract(self, text) -> Sentence:
        output = self.client.extract(text)

        result: Sentence = Sentence()
        result.text = text

        parts = output[1]

        tks = self._extract_tokens(parts['tokenized_text'])
        result.tokens.extend(tks)

        if (len(parts['relation_arcs_expanded']) > 0):
            rels = parts['relation_arcs_expanded']
            rs = self._extract_relations(tks, rels)
            result.relations.extend(rs)

        if (len(parts['ner']) > 0):
            ents = parts['ner']
#            for e in ents:
# result.append(self.entity(e))

        return result

    def _extract_tokens(self, tokens_json) -> Tokens:

        result: Tokens = Tokens()

        for i in range(0, len(tokens_json) - 1):
            text = tokens_json[i]
            idx = i

            tk: Token = Token(text)
            tk.lemma = text
            tk.position = idx

            result.append(tk)

        return result


    def _extract_relations(self, tokens: Tokens, relations_json) -> Relations:

        result: Relations = Relations()

        for rel in relations_json:
            left_begin_char = rel["arg1_begin_char"]
            left_end_char = rel["arg1_end_char"]
            left_begin_token = int(rel["arg1_begin_token"])
            left_end_token = int(rel["arg1_end_token"])
            left_text = rel["arg1_text"]

            right_begin_char = rel["arg2_begin_char"]
            right_end_char = rel["arg2_end_char"]
            right_begin_token = int(rel["arg2_begin_token"])
            right_end_token = int(rel["arg2_end_token"])
            right_text = rel["arg2_text"]

            relation_name = rel["type"]

            r = Relation()

            left_tokens = tokens[left_begin_token: left_end_token+1]
            right_tokens = tokens[right_begin_token: right_end_token+1]

            r.left.extend(left_tokens)
            r.right.extend(right_tokens)
            r.relation = relation_name

            result.append(r)

        return result


    def entity(self, entity):
        (type, token, text) = (entity['type'], entity['tokenized_text'], entity['text'])

        return "[" + text + ":" + type + "]"