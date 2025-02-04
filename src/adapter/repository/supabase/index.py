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

            self.logger.INFO(f"Connecting to Supabase")

            Client = create_client(
                self.settings.API_SUPABASE_URL, 
                self.settings.API_SUPABASE_KEY
            )

            self.logger.INFO(f"Connected to Supabase")
            
            return Client
        
        except Exception as e:
            self.logger.ERROR(f"Error connecting to Supabase: {e}")
    
    def getData(self, table: str) -> list:
        try:

            """
            Parameters: 
            - table (str): Nome da tabela;

            Returns:
            - data (list): Lista de dicionários com os dados da tabela selecionada.
            """

            client = self.__connect()
            
            self.logger.INFO(f"Getting data from table: {table}")
            
            data = client.from_(table).select("*").execute()

            self.logger.INFO(f"Data from table {table} retrieved successfully")
            
            return data.data
        
        except Exception as e:
            self.logger.ERROR(f"Error getting data from Supabase: {e}")
    

