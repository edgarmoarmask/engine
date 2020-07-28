from typing import List

import pandas as pd



class ColumnNames:

    @staticmethod
    def id():
        return "EntityId"

    @staticmethod
    def name():
        return "EntityName"

    @staticmethod
    def type():
        return "EntityType"

    @staticmethod
    def location():
        return "Location"

    @staticmethod
    def address():
        return "Address"

    @staticmethod
    def image():
        return "Image"


class Row:
    def __init__(self):
        empty_value = {ColumnNames.id(): 0,
                       ColumnNames.name(): "",
                       ColumnNames.type(): "",
                       ColumnNames.location(): "",
                       ColumnNames.address(): "",
                       ColumnNames.image(): ""
                       }

        self.to_row(empty_value)

    # TO ROW/RECORDS
    def to_record(self) -> {}:
        result = {ColumnNames.id(): self.id,
                  ColumnNames.name(): self.name,
                  ColumnNames.type(): self.type,
                  ColumnNames.location(): self.location,
                  ColumnNames.address(): self.address,
                  ColumnNames.image(): self.image
                  }

        return result

    def to_row(self, dataframe_row: {}):
        self.id = dataframe_row[ColumnNames.id()]
        self.name = dataframe_row[ColumnNames.name()]
        self.type = dataframe_row[ColumnNames.type()]
        self.location = dataframe_row[ColumnNames.location()]
        self.address = dataframe_row[ColumnNames.address()]
        self.image = dataframe_row[ColumnNames.image()]


    # PROPERTIES
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = value

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, value: str):
        self._image = value

class Rows(List[Row]):
    pass

class Storage:

    def __init__(self):
        self._table = {
            ColumnNames.id(): [],
            ColumnNames.name(): [],
            ColumnNames.type(): [],
            ColumnNames.location(): [],
            ColumnNames.address(): [],
            ColumnNames.image(): []
        }
        self._df: pd.DataFrame = pd.DataFrame(self._table)
        self._id = 0

    def get_storage_name(self):
        return "Entities"

    def add_record(self, name, type, location="", address="", image="") -> int:

        self._id = self._id + 1

        record = Row()
        record.id = self._id
        record.name = name
        record.type = type
        record.location = location
        record.address = address
        record.image = image

        record = record.to_record()
        self._df = self._df.append(record,ignore_index=True )

        return self._id


    def get_storage(self) -> pd.DataFrame:
        return self._df

    def find_by(self, column_name, column_value) -> Rows:
        df = self._df[self._df[column_name] == column_value]

        result = Rows()

        for i, r in df.iterrows():
            row = Row()
            row.to_row(r)

            result.append(row)

        return result

    def find_by_name(self, name):
        result = self.find_by(ColumnNames.name(), name)
        return result

    def find_by_id(self, id):
        result = self.find_by(ColumnNames.id(), id)
        return result

    def update_by_id(self, id, name, type, location="", address="", image=""):

        df = self._df
        row_id = df[ColumnNames.id()] == id

        df.loc[row_id, ColumnNames.name()] = name
        df.loc[row_id, ColumnNames.type()] = type
        df.loc[row_id, ColumnNames.location()] = location
        df.loc[row_id, ColumnNames.address()] = address
        df.loc[row_id, ColumnNames.image()] = image


    def drop_by_id(self, id):
        df = self._df

        row_id = df[ColumnNames.id()] == id

        self._df = df.drop(df[row_id].index)




