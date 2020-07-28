import os
from pathlib import Path


class IOUtils():
    @staticmethod
    def get_files_in_folder(folderName: str, fileExtension:str = "txt") -> list :
        r = list()

        for file in os.listdir(folderName):
            filename = os.fsdecode(file)
            if filename.endswith('.' + fileExtension):
                r.append(folderName + filename)

        return r


    @staticmethod
    def get_current_folder() -> str:
        result = str(Path.cwd())
        return result

    @staticmethod
    def get_subfolders(folderName) -> []:
        result = []
        for (rootDir, subDirs, files) in os.walk(folderName):
            for subDir in subDirs:
                result.append(subDir)

        return result

    @staticmethod
    def get_filename_without_extension(fileName: str) -> str:
        parts = os.path.splitext(fileName)
        return parts[0]

    @staticmethod
    def make_sure_folder_exists(folder_location: str):
        folder: Path = Path(folder_location)
        if (folder.exists() == False or folder.is_dir() == False):
            # create folder
            try:
                os.mkdir(folder_location)
            except OSError:
                print("Error creating folder: ", folder_location)
            else:
                print("Successfully create folder %s" % folder_location)



