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

            # # Inicializa as colunas como strings vazias
            # df["poloAtivoNome"] = ""
            # df["poloAtivoTipo"] = ""
            # df["poloAtivoCPF"] = ""
            # df["poloAtivoCNPJ"] = ""

            # df["poloPassivoNome"] = ""
            # df["poloPassivoTipo"] = ""
            # df["poloPassivoCPF"] = ""
            # df["poloPassivoCNPJ"] = ""

            # # Itera sobre a lista de dicionários
            # for item in dictData:
            #     if "poloAtivo" in item:
            #         self.logger.INFO(f"Processing data from process number: {item['numeroProcesso']}")
            #         nomesAtivo = []
            #         tiposAtivo = []
            #         cpfsAtivo = []
            #         cnpjsAtivo = []

            #         # Itera sobre os envolvidos no polo ativo
            #         for envolvido in item["poloAtivo"]:
            #             self.logger.INFO(f"Processing data from envolved: {envolvido.get('nome', '')}")
            #             nomesAtivo.append(envolvido.get("nome", "") or "")
            #             tiposAtivo.append(envolvido.get("tipo", "") or "")
            #             cpfsAtivo.append(envolvido.get("cpf", "") or "")
            #             cnpjsAtivo.append(envolvido.get("cnpj", "") or "")

            #         # Atualiza as colunas com os valores concatenados
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloAtivoNome"] = ", ".join(nomesAtivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloAtivoTipo"] = ", ".join(tiposAtivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloAtivoCPF"] = ", ".join(cpfsAtivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloAtivoCNPJ"] = ", ".join(cnpjsAtivo)

            #     if "poloPassivo" in item:
            #         self.logger.INFO(f"Processing data from process number: {item['numeroProcesso']}")
            #         nomesPassivo = []
            #         tiposPassivo = []
            #         cpfsPassivo = []
            #         cnpjsPassivo = []

            #         # Itera sobre os envolvidos no polo passivo
            #         for envolvido in item["poloPassivo"]:
            #             self.logger.INFO(f"Processing data from envolved: {envolvido.get('nome', '')}")
            #             nomesPassivo.append(envolvido.get("nome", "") or "")
            #             tiposPassivo.append(envolvido.get("tipo", "") or "")
            #             cpfsPassivo.append(envolvido.get("cpf", "") or "")
            #             cnpjsPassivo.append(envolvido.get("cnpj", "") or "")

            #         # Atualiza as colunas com os valores concatenados
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloPassivoNome"] = ", ".join(nomesPassivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloPassivoTipo"] = ", ".join(tiposPassivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloPassivoCPF"] = ", ".join(cpfsPassivo)
            #         df.loc[df["numeroProcesso"] == item["numeroProcesso"], "poloPassivoCNPJ"] = ", ".join(cnpjsPassivo)

            df["typeTribunal"] = df["tribunal"].str.split("-").str[0].str.lower()
            df["endpoint"] = df["tribunal"].str.split("-").str[1]

            df["numeroProcessoFormated"] = df["numeroProcesso"].apply(self.dataframe.removeSpecialCharacters)
            
            self.logger.INFO("Data from Escavador loaded")
            return df
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