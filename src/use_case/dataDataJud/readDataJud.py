
import json


from src.adapter.core.config import Settings
from src.adapter.dataframe.interface import IDataFrameAdapter
from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils


class ReadDataJud:
    def __init__(self, dataframe: IDataFrameAdapter):
        self.logger = LoggerHandler("ReadDataJud")
        self.dataframe = dataframe
        self.settings = Settings()
        self.utils = Utils()

    def readDataJud(self):
        try:
            self.logger.INFO("Reading data from DataJud DataLake")
            results = []

            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_{self.utils.getToday()}.json", "r"
                )
            )

            dictData


        except Exception as e:
            self.logger.ERROR(f"Error in readDataJud: {e}")
            return None