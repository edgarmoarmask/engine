

class OpenIeFormatter:
    @staticmethod
    def extract_relations(openie_output):
        for e in openie_output:
            confidence = e['confidence']
            if (confidence < 0.5):
                continue

            rel = e['extraction']['rel']['text']
            a1 = e['extraction']['arg1']['text']
            arg2s = e['extraction']['arg2s']
            a2 = ""
            for a in arg2s:
                if (len(a2)!= 0):
                    a2 = a2 + ","
                a2 = a2 + a['text']

            summary = "[" + a1, " , " + rel + " , " + a2 + "]"
            conf = str(confidence)
            print("openie-relation: " , summary  , " " , conf )

