import datetime
from typing import List

import pandas as pd



class ColumnNames:

    @staticmethod
    def event_id():
        return "EventId"

    @staticmethod
    def doc_id():
        return "DocId"

    @staticmethod
    def entity_one_id():
        return "Entity1Id"

    @staticmethod
    def entity_two_id():
        return "Entity2Id"

    @staticmethod
    def date():
        return "Date"


class Row:
    def __init__(self):
        empty_value = {
                       ColumnNames.doc_id(): 0,
                       ColumnNames.event_id(): 0,
                       ColumnNames.entity_one_id(): 0,
                       ColumnNames.entity_two_id(): 0,
                       ColumnNames.date(): datetime.datetime.now()
                       }

        self.to_row(empty_value)

    # TO ROW/RECORDS
    def to_record(self) -> {}:
        result = {
                  ColumnNames.doc_id(): self.doc_id,
                  ColumnNames.event_id(): self.event_id,
                  ColumnNames.entity_one_id(): self.entity_one_id,
                  ColumnNames.entity_two_id(): self.entity_two_id,
                  ColumnNames.date(): self.date
                  }

        return result

    def to_row(self, dataframe_row: {}):
        self.doc_id = dataframe_row[ColumnNames.doc_id()]
        self.event_id = dataframe_row[ColumnNames.event_id()]
        self.entity_one_id = dataframe_row[ColumnNames.entity_one_id()]
        self.entity_two_id = dataframe_row[ColumnNames.entity_two_id()]
        self.date = dataframe_row[ColumnNames.date()]


    # PROPERTIES
    @property
    def event_id(self) -> int:
        return self._event_id

    @event_id.setter
    def event_id(self, value: int):
        self._event_id = value

    @property
    def doc_id(self) -> int:
        return self._doc_id

    @doc_id.setter
    def doc_id(self, value: int):
        self._doc_id = value

    @property
    def entity_one_id(self) -> int:
        return self._entity_one_id

    @entity_one_id.setter
    def entity_one_id(self, value: int):
        self._entity_one_id = value

    @property
    def entity_two_id(self) -> int:
        return self._entity_two_id

    @entity_two_id.setter
    def entity_two_id(self, value: int):
        self._entity_two_id = value

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
            ColumnNames.event_id(): [],
            ColumnNames.entity_one_id(): [],
            ColumnNames.entity_two_id(): [],
            ColumnNames.date(): []
        }
        self._df: pd.DataFrame = pd.DataFrame(self._table)

    def get_storage_name(self):
        return "EventMentions"

    def add_record(self, event_id, doc_id, entity_one_id, entity_two_id, date) -> (int, int):

        record = Row()
        record.event_id = event_id
        record.doc_id = doc_id
        record.entity_one_id = entity_one_id
        record.entity_two_id = entity_two_id
        record.date = date

        record = record.to_record()
        self._df = self._df.append(record,ignore_index=True )

        return (event_id, doc_id)


    def get_storage(self) -> pd.DataFrame:
        return self._df

    def find_by_ids(self, event_id, doc_id):

        result = Rows()

        df = self._df[self._df[ColumnNames.event_id()] == event_id]
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



