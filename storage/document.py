from typing import List

import pandas as pd
import datetime


class ColumnNames:

    @staticmethod
    def id():
        return "DocId"

    @staticmethod
    def name():
        return "DocName"

    @staticmethod
    def location():
        return "DocLocation"

    @staticmethod
    def date():
        return "Date"

    @staticmethod
    def text():
        return "Text"

class Row:
    def __init__(self):
        empty_value = {
                       ColumnNames.id(): 0,
                       ColumnNames.name(): "",
                       ColumnNames.location(): "",
                       ColumnNames.date(): datetime.datetime.now(),
                       ColumnNames.text(): ""
                       }

        self.to_row(empty_value)

    # TO ROW/RECORDS
    def to_record(self) -> {}:
        result = {
            ColumnNames.id(): self.id,
            ColumnNames.name(): self.name,
            ColumnNames.location(): self.location,
            ColumnNames.date(): self.date,
            ColumnNames.text(): self.text
        }

        return result

    def to_row(self, dataframe_row: {}):
        self.id = dataframe_row[ColumnNames.id()]
        self.name = dataframe_row[ColumnNames.name()]
        self.location = dataframe_row[ColumnNames.location()]
        self.date = dataframe_row[ColumnNames.date()]
        self.text = dataframe_row[ColumnNames.text()]

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
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = value

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: datetime):
        self._date = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value



class Rows(List[Row]):
    pass

class Storage:

    def __init__(self):
        self._table = {ColumnNames.id(): [],
                       ColumnNames.name(): [],
                       ColumnNames.location(): [],
                       ColumnNames.date(): [],
                       ColumnNames.text(): []
                       }
        self._df: pd.DataFrame = pd.DataFrame(self._table)
        self._id = 0

    def get_storage_name(self):
        return "Documents"

    def add_record(self, name, location, date, text) -> int:

        self._id = self._id + 1

        record = Row()
        record.id = self._id
        record.name = name
        record.location = location
        record.date= date
        record.text = text

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

    def update_by_id(self, id, name, location, date, text ):

        df = self._df
        row_id = df[ColumnNames.id()] == id

        df.loc[row_id, ColumnNames.name()] = name
        df.loc[row_id, ColumnNames.location()] = location
        df.loc[row_id, ColumnNames.date()] = date
        df.loc[row_id, ColumnNames.text()] = text

    def drop_by_id(self, id):
        df = self._df

        row_id = df[ColumnNames.id()] == id

        self._df = df.drop(df[row_id].index)


