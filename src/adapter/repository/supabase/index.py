from supabase import create_client, Client

from src.adapter.core.config import Settings
from src.adapter.logging.logging import LoggerHandler


"""
Conexão com o banco de dados do Supabase
"""


class Supabase():
    def __init__(self):
        self.logger = LoggerHandler("Supabase")
        self.settings = Settings()
        
    def __connect(self) -> Client:
        try:

            """
            Conecta ao banco de dados do Supabase
            """

            self.logger.INFO(f"Connecting to Supabase: {self.settings.API_SUPABASE_URL}")

            Client = create_client(
                self.settings.API_SUPABASE_URL, 
                self.settings.API_SUPABASE_KEY
            )

            self.logger.INFO(f"Connected to Supabase")
            
            return Client
        
        except Exception as e:
            self.logger.ERROR(f"Error connecting to Supabase: {e}")
    
    def getData(self, table: str, activedFilter: str = None) -> list:
        try:

            """
            Parameters: 
            - table (str): Nome da tabela;

            Returns:
            - data (list): Lista de dicionários com os dados da tabela selecionada.
            """

            client = self.__connect()
            
            self.logger.INFO(f"Getting data from table: {table}")

            if activedFilter is not None:
                self.logger.INFO(f"Filtering data by actived: {activedFilter}")
                
                data = client.from_(table).select("*").eq("active", activedFilter).execute()
            
            else:
                self.logger.INFO(f"Filtering data isn't informed")
                
                data = client.from_(table).select("*").execute()

            self.logger.INFO(f"Data from table {table} retrieved successfully")
            
            return data.data
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from Supabase: {e}")
    

    def getBucket(self, bucket: str = None) -> list:
        try:

            """
            Parameters: 
            - bucket (str): Nome do bucket;

            Returns:
            - data (list): Lista de dicionários com os dados do bucket selecionado.
            """

            client = self.__connect()
            
            self.logger.INFO(f"Getting data from bucket: {bucket}")
            
            data = client.storage.list_buckets()
            
            self.logger.INFO(f"Data from bucket {bucket} retrieved successfully")
            
            return data
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from bucket: {e}")