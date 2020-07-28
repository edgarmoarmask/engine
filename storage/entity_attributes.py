from typing import List

import pandas as pd

class ColumnNames:

    @staticmethod
    def id():
        return "EntityId"

    @staticmethod
    def name():
        return "AttributeName"

    @staticmethod
    def value():
        return "AttributeValue"

    @staticmethod
    def doc_id():
        return "DocId"


class Row:
    def __init__(self):
        empty_value = {
            ColumnNames.id(): 0,
            ColumnNames.name(): "",
            ColumnNames.value(): "",
            ColumnNames.doc_id(): 0
        }

        self.to_row(empty_value)

    # TO ROW/RECORDS
    def to_record(self) -> {}:
        result = {
            ColumnNames.id(): self.id,
            ColumnNames.name(): self.name,
            ColumnNames.value(): self.value,
            ColumnNames.doc_id(): self.doc_id

            }

        return result

    def to_row(self, dataframe_row: {}):
        self.id = dataframe_row[ColumnNames.id()]
        self.name = dataframe_row[ColumnNames.name()]
        self.value = dataframe_row[ColumnNames.value()]
        self.doc_id = dataframe_row[ColumnNames.doc_id()]

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
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @property
    def doc_id(self) -> int:
        return self._doc_id

    @doc_id.setter
    def doc_id(self, value: int):
        self._doc_id = value

class Rows(List[Row]):
    pass

class Storage:

    def __init__(self):
        self._table = {
            ColumnNames.id(): [],
            ColumnNames.name(): [],
            ColumnNames.value(): [],
            ColumnNames.doc_id(): []
        }
        self._df: pd.DataFrame = pd.DataFrame(self._table)
        self._id = 0

    def get_storage_name(self):
        return "EntityAttributes"


    def add_record(self, name, value, doc_id) -> int:

        self._id = self._id + 1

        record = Row()
        record.id = self._id
        record.name = name
        record.value = value
        record.doc_id = doc_id


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

    def update_by_id(self, id, name, value, doc_id):

        df = self._df
        row_id = df[ColumnNames.id()] == id

        df.loc[row_id, ColumnNames.name()] = name
        df.loc[row_id, ColumnNames.value()] = value
        df.loc[row_id, ColumnNames.doc_id()] = doc_id

    def drop_by_id(self, id):
        df = self._df

        row_id = df[ColumnNames.doc_id()] == id

        self._df = df.drop(df[row_id].index)




