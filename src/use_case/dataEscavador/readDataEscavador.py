import json
from datetime import datetime


from src.adapter.core.config import Settings
from src.adapter.dataframe.interface import IDataFrameAdapter
from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils


class ReadEscavador():
    def __init__(self, dataframe: IDataFrameAdapter):
        self.logger = LoggerHandler("ReadEscavador")
        self.dataframe = dataframe
        self.settings = Settings()
        self.utils = Utils()

    def getData(self):
        try:
            self.logger.INFO("Getting data from Escavador")
            
            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_escavador_{self.utils.getToday().month}_{self.utils.getToday().year}.json", "r"
                )
            )

            df = self.dataframe.to_DataFrame(dictData)
            self.logger.INFO("Data read successfully")
            
            self.logger.INFO("Data from Escavador loaded")
            return df
        except Exception as e:
            self.logger.ERROR(f"Error getting data from Escavador: {e}")
            return None
        
