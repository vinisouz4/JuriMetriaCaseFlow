from src.adapter.dataframe.interface import IDataFrameAdapter
from src.adapter.repository.supabase.index import Supabase
from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils
import json



class ReadCaseFlowData():
    def __init__(self, dataframe: IDataFrameAdapter):
        self.logger = LoggerHandler("ReadCaseFlowData")
        self.utils = Utils()
        self.dataframe = dataframe
        self.supabase = Supabase()
        

    def getData(self, table: str, activedFilter: str = None):
        self.logger.INFO("Reading data from Supabase")
        
        data = self.supabase.getData(table, activedFilter)

        dfData = self.dataframe.to_DataFrame(data)

        dfData["value_cause"] = dfData["value_cause"].apply(self.dataframe.convertToFloat)
        
        return dfData
