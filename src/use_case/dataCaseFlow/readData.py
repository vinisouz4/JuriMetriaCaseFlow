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
        

    def getData(self, table: str, activedFilter: str = None, removeSpecialCharacters: bool = False):
        """
        Parameters:
        - table (str): Nome da tabela;
        - activedFilter (str): Filtro de ativo;
        - removeSpecialCharacters (bool): Remover caracteres especiais da coluna de external_number
        """
        self.logger.INFO("Reading data from Supabase")
        
        data = self.supabase.getData(table, activedFilter)

        dfData = self.dataframe.to_DataFrame(data)

        if removeSpecialCharacters:
            self.logger.INFO("Removing special characters from external_number")
            dfData["external_number"] = dfData["external_number"].apply(self.dataframe.removeSpecialCharacters)
            self.logger.INFO("Special characters removed")

        dfData["value_cause"] = dfData["value_cause"].apply(self.dataframe.convertToFloat)
        
        return dfData
    
    def getClients(self, table):
        try:
            self.logger.INFO("Reading data from Supabase")
            
            data = self.supabase.getData(table)
            
            self.logger.INFO(f"Len data {len(data)}")
            
            df = self.dataframe.to_DataFrame(data)
            
            df = df[["id", "name", "cpf_cnpj"]]

            dfFinal = df[df["cpf_cnpj"].apply(self.utils.validateDoc)]

            dfFinal["cpf_cnpj"] = dfFinal["cpf_cnpj"].str.replace('.', '').str.replace('-', '').str.replace('/', '')
            
            self.logger.INFO("Data read successfully")
            return dfFinal
        
        except Exception as e:
            self.logger.ERROR(f"Error reading data from Supabase: {e}")
            return None