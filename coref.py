from lib.docs.newsDocument import NewsDocument
from lib.extractors.corenlp import CoreNlpExtractor
from lib.nlp.coreference import Coreference
from utils import get_cases_folder, get_cases_files
from lib.utils.ioutils import IOUtils


class Coref:
    @staticmethod
    def coref():
        cases_folder = get_cases_folder()
        cases_files = get_cases_files()

        coref = Coreference()

        for cs in cases_files:
            files = cases_files[cs]

            for f in files:
                try:
                    doc_file = open(IOUtils.get_filename_without_extension(f) + ".coref", "w+")
                    doc_file.flush()
                    doc = NewsDocument.Load(f)
                    doc_file.write(coref.resolve(doc.text))
                except Exception:
                    print("issue -> ", f)
                finally:
                    print(f)
                    doc_file.close()

    @staticmethod
    def coref_corenlp():
        cases_folder = get_cases_folder()
        cases_files = get_cases_files()

        corenlp_extractor = CoreNlpExtractor()

        for cs in cases_files:
            files = cases_files[cs]

            for f in files:
                try:
                    doc_file = open(IOUtils.get_filename_without_extension(f) + ".corenlp-coref", "w+")
                    doc_file.flush()
                    doc = NewsDocument.Load(f)

                    sents = corenlp_extractor.extract(doc.text)



                except Exception:
                    print("issue -> ", f)
                finally:
                    print(f)
                    doc_file.close()