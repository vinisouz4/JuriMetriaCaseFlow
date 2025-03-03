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

            df["typeTribunal"] = df["tribunal"].str.split("-").str[0].str.lower()
            df["endpoint"] = df["tribunal"].str.split("-").str[1]

            df["numeroProcessoFormated"] = df["numeroProcesso"].apply(self.dataframe.removeSpecialCharacters)

            dfExploded = self.dataframe.json_normaliza(df, "dataPoloAtivo", suffix="Ativo", listDropColum=['dataPoloAtivo', "nomeAtivo", "AtivoAtivo"])
            dfExploded = self.dataframe.json_normaliza(dfExploded, "dataPoloPassivo", suffix="Passivo", listDropColum=['dataPoloPassivo', "nomePassivo", "PassivoPassivo"])
            
            self.logger.INFO("Data from Escavador loaded")
            return dfExploded
        except Exception as e:
            self.logger.ERROR(f"Error getting data from Escavador: {e}")
            return None
        
    def processAtivoPassivo(self, df, processNumber: str = None):
        try:

            """
            Método para buscar quem são os polos ativos e passivos e retornar os dois polos.
            """

            self.logger.INFO("Processing data from Escavador")
            
            if processNumber is None or processNumber == "":
                self.logger.INFO("Filtering data by process number: None")
                return "Informar o número do processo", "Informar o número do processo"
            
            else:
                self.logger.INFO(f"Filtering data by process number: {processNumber}")
                
                df = df[df["numeroProcessoFormated"] == processNumber]

                return df["poloAtivo"].values[0], df["poloPassivo"].values[0]

        except Exception as e:
            self.logger.ERROR(f"Error processing data from Escavador: {e}")
            return None
        
    def totalTribunal(self, df, processNumber: str = None, tribunal: list = None, client: str = None):
        try:
            self.logger.INFO("Getting total of tribunals")

            if tribunal is not None and tribunal != []:
                self.logger.INFO(f"Filtering data by tribunal: {tribunal}")
                df = df[
                    df["tribunal"].isin(tribunal)
                ]

                dfGrouped = df.groupby('tribunal').size().reset_index(name='Total')

                dfGrouped.rename(
                    columns={
                        "tribunal": "Tribunal"
                    }, 
                    inplace=True
                )
                
                self.logger.INFO("Total of tribunals counted successfully")    
                
                return dfGrouped
            
            else:
                self.logger.INFO("No filter by tribunal")

                dfGrouped = df.groupby('tribunal').size().reset_index(name='Total')

                dfGrouped.rename(
                    columns={
                        "tribunal": "Tribunal"
                    }, 
                    inplace=True
                )

                self.logger.INFO("Total of tribunals counted successfully")

                return dfGrouped
            
        except Exception as e:
            self.logger.ERROR(f"Error getting total of tribunals: {e}")
            return None

    def totalClient(self, df, processNumber: str = None, client: str = None, clientHvk = list):
        try:
            self.logger.INFO("Getting total of clients")

            df = self.utils.findClient(df, clientHvk)

            if processNumber != "" and processNumber is not None or client != "" and client is not None:
                self.logger.INFO(f"Filtering data by process number: {processNumber}")
                df = df[
                    df["numeroProcessoFormated"] == processNumber
                ]

                self.logger.INFO(f"Filtering data by client: {client}")
                df = df[
                    df["cpf_cnpj"] == client
                ]

                dfGrouped = df.groupby('name').size().reset_index(name='Total')
                
                self.logger.INFO("Total of clients counted successfully")    
                
                return dfGrouped
            
            else:
                self.logger.INFO("No filter by client")

                

                # dfGrouped = df.groupby('name').size().reset_index(name='Total')

                # dfGrouped.rename(
                #     columns={
                #         "name": "Cliente"
                #     }, 
                #     inplace=True
                # )

                # self.logger.INFO("Total of clients counted successfully")

                return df
            
        except Exception as e:
            self.logger.ERROR(f"Error getting total of clients: {e}")
            return None