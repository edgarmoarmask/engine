
from pyopenie import OpenIE5

client_openie = OpenIE5('http://localhost:8111')




class Extractor:
    def __init__(self, server, port):
        url = server + ":" + str(port)
        self.client = OpenIE5(url)

    def extract(self, text) -> [str]:

        output = self.client.extract(text=text)

        result = [str]

        for rel in output:
            result.append(self.relation(rel))

        return result


    def relation(self, relation) -> str:
        confidence = relation['confidence']

        rel = relation['extraction']['rel']['text']
        a1 = relation['extraction']['arg1']['text']
        arg2s = relation['extraction']['arg2s']
        a2 = ""
        for a in arg2s:
            if (len(a2) != 0):
                a2 = a2 + ","
            a2 = a2 + a['text']

        conf = str(confidence)
        return "openie-relation [" + a1, " , " + rel + " , " + a2 + "] " + conf