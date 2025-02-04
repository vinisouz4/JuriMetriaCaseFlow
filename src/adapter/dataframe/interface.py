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