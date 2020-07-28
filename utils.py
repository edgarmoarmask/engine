from lib.utils.ioutils import IOUtils
from pathlib import Path

def get_cases_folder() -> str:
    root_folder = IOUtils.get_current_folder()
    result  = root_folder + '/datasets/UnderDev'
    return result

def get_cases_subfolders() -> str:
    result = IOUtils.get_subfolders(get_docs_folder())
    return result

def get_cases_files(file_extension="txt"):
    cases_folder = get_docs_folder()
    subfolders = get_cases_subfolders()

    result = {}

    for s in subfolders:
        caseFolder = cases_folder + "/" + s + "/"

        files = IOUtils.get_files_in_folder(caseFolder, file_extension)

        result[s] = files

    return result

def get_docs_folder():
    root = IOUtils.get_current_folder()

    folder = str(Path(root).parents[0]) #->
    folder = folder + "/" + "docs"

    return folder

def get_db_folder():
    root = IOUtils.get_current_folder()

    folder = str(Path(root).parents[0])  # ->
    folder = folder + "/" + "db"

    return folder
