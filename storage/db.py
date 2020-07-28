from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

import storage.document as doc
import storage.entity_types as etypes
import storage.entity as entity
import storage.entity_mentions as entity_mentions
import storage.event_types as event_types
import storage.event_mentions as event_mentions
import storage.entity_attributes as entity_attributes
from lib.utils.ioutils import IOUtils

from utils import get_db_folder


class Db:
    def __init__(self, db_name = ""):

        self._db_name = db_name

        self._doc: doc.Storage = doc.Storage()
        self._entity_types: etypes.Storage = etypes.Storage()
        self._entities : entity.Storage = entity.Storage()
        self._entity_mentions: entity_mentions.Storage = entity_mentions.Storage()
        self._event_types: event_types.Storage = event_types.Storage()
        self._event_mentions : entity_mentions.Storage = event_mentions.Storage()
        self._entity_attributes: entity_attributes.Storage = entity_attributes.Storage()
    @property
    def documents(self) -> doc.Storage:
        return self._doc

    @property
    def entity_types(self) -> etypes.Storage:
        return self._entity_types

    @property
    def entities(self) -> entity.Storage:
        return self._entities

    @property
    def entity_mentions(self) -> entity_mentions.Storage:
        return self._entity_mentions

    @property
    def event_types(self) -> event_types.Storage:
        return self._event_types

    @property
    def event_mentions(self) -> event_mentions.Storage:
        return self._event_mentions

    @property
    def entity_attributes(self) -> entity_attributes.Storage:
        return self._entity_attributes


    def save(self,file_name = 'EagleyeSampleDb.xlsx', ):

        wb = load_workbook('Eagleye-Blank-Blank.xlsx')

        self.__save_storage(self.documents.get_storage(), self.documents.get_storage_name(), wb)
        self.__save_storage(self.entity_types.get_storage(), self.entity_types.get_storage_name(), wb)
        self.__save_storage(self.entities.get_storage(), self.entities.get_storage_name(), wb)
        self.__save_storage(self.entity_attributes.get_storage(), self.entity_attributes.get_storage_name(), wb)
        self.__save_storage(self.entity_mentions.get_storage(), self.entity_mentions.get_storage_name(), wb)
        self.__save_storage(self.event_types.get_storage(), self.event_types.get_storage_name(), wb)
        self.__save_storage(self.event_mentions.get_storage(), self.event_mentions.get_storage_name(), wb)


        folder = self._db_name
        if folder == "":
            folder = get_db_folder()

        IOUtils.make_sure_folder_exists(folder_location=folder)


        file_name = folder + "/" + file_name
        wb.save(file_name)

    def __save_storage(self, df: pd.DataFrame, storage_name: str,  wb: Workbook):
        sheet = wb[storage_name]

        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)