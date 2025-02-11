import abc

class IDataFrameAdapter(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def read_csv(self, path: str):
        pass

    @abc.abstractmethod
    def to_DataFrame(self, data: list):
        pass

    @abc.abstractmethod
    def to_datetime(self, data, column: list):
        pass

    @abc.abstractmethod
    def getPastDate(self, days: int, today):
        pass

    @abc.abstractmethod
    def groupby(self, df, columns: list, agg: dict):
        pass

    @abc.abstractmethod
    def convertToFloat(self, value: str) -> float:
        pass

    @abc.abstractmethod
    def removeSpecialCharacters(self, value: str) -> str:
        pass