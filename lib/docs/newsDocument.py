from datetime import datetime
from lib.docs.document import Document



class NewsDocument():

    @staticmethod
    def Load(fileName) -> Document:
        title = ""
        date = datetime.now()
        text = ''

        with open(fileName, "r", encoding="utf-8") as f:
            for line in f:

                if line.startswith("Title"):
                    parts = line.split(":")
                    clean_str = parts[1].translate({ord('\n'): None})
                    title = clean_str.strip()
                elif line.startswith("Date"):
                    parts = line.split(":")
                    clean_str = parts[1].translate({ord('\n'): None})
                    date = datetime.now()
                    clean_str = clean_str.strip()
                    try:
                        date = datetime.strptime(clean_str, "%d %B %Y")
                    except Exception as e:
                        print("DATE PARSING ERROR: ",  fileName, "->", clean_str, " exception: ", str(e) )

                elif line != "\n":
                    text = text + line

        document = Document(title=title, text=text)
        document.date = date

        return document

    @staticmethod
    def GetFileContent(fileName):
        text = ''
        with open(fileName, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Title"):
                    parts = line.split(":")
                    clean_str = parts[1].translate({ord('\n'): None})
                    title = clean_str.strip()
                elif line.startswith("Date"):
                    parts = line.split(":")
                    clean_str = parts[1].translate({ord('\n'): None})
                    date = datetime.strptime(clean_str.strip(), "%d %B %Y")
                elif line != "\n":
                    text = text + line

        return text
