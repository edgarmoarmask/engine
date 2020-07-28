from crawler import Crawler
from utils import get_cases_files, get_db_folder

if __name__ == '__main__':
    cases_files = get_cases_files("txt")

    for folder_name in cases_files:
        doc_files = cases_files[folder_name]
        full_folder_name = get_db_folder() + "/" + folder_name
        crawler = Crawler(full_folder_name, doc_files)
        crawler.crawl()

    print("DONE CRAWLING!!!")