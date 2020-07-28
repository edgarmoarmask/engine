from typing import List

import pandas as pd
import datetime


class ColumnNames:

    @staticmethod
    def entity_id():
        return "EntityId"

    @staticmethod
    def doc_id():
        return "DocId"

    @staticmethod
    def start_index():
        return "StartIndex"

    @staticmethod
    def end_index():
        return "EndIndex"

    @staticmethod
    def date():
        return "Date"


class Row:
    def __init__(self):
        empty_value = {
                       ColumnNames.doc_id(): 0,
                       ColumnNames.entity_id(): 0,
                       ColumnNames.start_index(): 0,
                       ColumnNames.end_index(): 0,
                       ColumnNames.date(): datetime.datetime.now()
                       }

        self.to_row(empty_value)

    # TO ROW/RECORDS
    def to_record(self) -> {}:
        result = {
                  ColumnNames.doc_id(): self.doc_id,
                  ColumnNames.entity_id(): self.entity_id,
                  ColumnNames.start_index(): self.start_index,
                  ColumnNames.end_index(): self.end_index,
                  ColumnNames.date(): self.date
                  }

        return result

    def to_row(self, dataframe_row: {}):
        self.doc_id = dataframe_row[ColumnNames.doc_id()]
        self.entity_id = dataframe_row[ColumnNames.entity_id()]
        self.start_index = dataframe_row[ColumnNames.start_index()]
        self.end_index = dataframe_row[ColumnNames.end_index()]
        self.date = dataframe_row[ColumnNames.date()]


    # PROPERTIES
    @property
    def entity_id(self) -> int:
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value: int):
        self._entity_id = value

    @property
    def doc_id(self) -> int:
        return self._doc_id

    @doc_id.setter
    def doc_id(self, value: int):
        self._doc_id = value

    @property
    def start_index(self) -> int:
        return self._start_index

    @start_index.setter
    def start_index(self, value: int):
        self._start_index = value

    @property
    def end_index(self) -> int:
        return self._end_index

    @end_index.setter
    def end_index(self, value: int):
        self._end_index = value

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: datetime):
        self._date = value


class Rows(List[Row]):
    pass

class Storage:

    def __init__(self):
        self._table = {
            ColumnNames.doc_id(): [],
            ColumnNames.entity_id(): [],
            ColumnNames.start_index(): [],
            ColumnNames.end_index(): [],
            ColumnNames.date(): []
        }
        self._df: pd.DataFrame = pd.DataFrame(self._table)

    def get_storage_name(self):
        return "EntityMentions"

    def add_record(self, entity_id, doc_id, start_index, end_index, date) -> (int, int):

        record = Row()
        record.entity_id = entity_id
        record.doc_id = doc_id
        record.start_index = start_index
        record.end_index = end_index
        record.date = date

        record = record.to_record()
        self._df = self._df.append(record,ignore_index=True )

        return (entity_id, doc_id)


    def get_storage(self) -> pd.DataFrame:
        return self._df

    def find_by_ids(self, entity_id, doc_id):

        result = Rows()

        df = self._df[self._df[ColumnNames.entity_id()] == entity_id]
        df = df[df[ColumnNames.doc_id()]== doc_id]

        for i, r in df.iterrows():
            row = Row()
            row.to_row(r)

            result.append(row)

        return result

    def update_by_id(self, entity_id, doc_id, start_index, end_index):
        """
                df = self._df
                row_id = df[ColumnNames.id() ] == id

                df.loc[row_id, ColumnNames.name()] = name
                df.loc[row_id, ColumnNames.type()] = type
                df.loc[row_id, ColumnNames.location()] = location
                df.loc[row_id, ColumnNames.address()] = address
                df.loc[row_id, ColumnNames.image()] = image
        """
        pass

    def drop_by_id(self, id):
        """
        df = self._df

        row_id = df[ColumnNames.id()] == id

        self._df = df.drop(df[row_id].index)
        """
        pass



