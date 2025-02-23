
import json
from datetime import datetime
from itertools import product


from src.adapter.core.config import Settings
from src.adapter.dataframe.interface import IDataFrameAdapter
from src.adapter.logging.logging import LoggerHandler
from src.utils.utils import Utils


class ReadDataJud():
    def __init__(self, dataframe: IDataFrameAdapter):
        self.logger = LoggerHandler("ReadDataJud")
        self.dataframe = dataframe
        self.settings = Settings()
        self.utils = Utils()

    def readDataJud(self):
        try:

            """
            Metodo para buscar apenas o ultimo movimento de cada processo
            """

            self.logger.INFO(f"Reading data from DataJud DataLake, Date: {self.utils.getToday()}")

            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_{self.utils.getToday().month}_{self.utils.getToday().year}.json", "r"
                )
            )

            self.logger.INFO("Data read successfully")

            resultado = []
            notFound = []

            for process in dictData:
                if process["data"]["hits"]["hits"] == []:
                    notFound.append({
                        "processo": process["processo"],
                        "hits": 0
                    })
                else:
                    for source in process["data"]["hits"]["hits"]:
                        movimentos = source["_source"].get("movimentos", [])
                        if movimentos:
                            ultimo_movimento = max(movimentos, key=lambda x: datetime.strptime(x["dataHora"], "%Y-%m-%dT%H:%M:%S.%fZ"))

                            results = {
                                "processo": source["_source"]["numeroProcesso"],
                                "dataAjuizamento": source["_source"]["dataAjuizamento"],
                                "dataUltimoMovimento": ultimo_movimento["dataHora"],
                                "movimento": ultimo_movimento["nome"]
                            }

                            resultado.append(results)


            self.logger.INFO("Transforming data to DataFrame")

            df = self.dataframe.to_DataFrame(resultado)

            df = self.dataframe.to_datetime(df, ["dataUltimoMovimento", "dataAjuizamento"])

            dfNotFound = self.dataframe.to_DataFrame(notFound)

            self.logger.INFO("Data transformed successfully")

            return df, dfNotFound

        except Exception as e:
            self.logger.ERROR(f"Error in readDataJud: {e}")
            return None

    def getAllMoviments(self):
        try:

            """
            Metodo para buscar todas as movimentacoes e datas de cada movimentacao.
            """

            self.logger.INFO(f"Reading data from DataJud DataLake, Date: {self.utils.getToday()}")

            dictData = json.load(
                open(
                    f"{self.settings.DATALAKE_URL}data_{self.utils.getToday().month}_{self.utils.getToday().year}.json", "r"
                )
            )

            self.logger.INFO("Data read successfully")

            processoFormatado =[]

            for process in dictData:
                for source in process["data"]["hits"]["hits"]:
                    sources = source["_source"]
                    processo = {
                        "numeroProcesso": sources.get("numeroProcesso", ""),
                        "dataAjuizamento": self.utils.formatar_data(sources.get("dataAjuizamento", "")),
                    }

                    movimentos_ordenados = sorted(
                        sources.get("movimentos", []),
                        key=lambda x: x["dataHora"]
                    )

                    processo["movimentos"] = [mov["nome"] for mov in movimentos_ordenados]
                    processo["dataMovimentacao"] = [self.utils.formatar_data(mov["dataHora"]) for mov in movimentos_ordenados]

                    processoFormatado.append(processo)

            df = self.dataframe.to_DataFrame(processoFormatado)

            self.logger.INFO("Data transformed successfully")

            return df

        except Exception as e:
            self.logger.ERROR(f"Error in readDataJud: {e}")
            return None
        
    def totalStatus(self, df, numberProcess: str = None):
        try:

            """
            Método para contar a quantidade de processos por status
            """

            self.logger.INFO("Starting totalStatus")

            if numberProcess is not None and numberProcess != "":
                self.logger.INFO(f"Filtering data by process number: {numberProcess}")
                
                df = df[
                    df["numeroProcesso"] == numberProcess
                ]
                
                data = df.groupby('movimentos').size().reset_index(name='total')
                
                self.logger.INFO("Status counted successfully")
                
                return data

            else:
                self.logger.INFO("Filtering data by process number: None")

                data = df.groupby('movimentos').size().reset_index(name='total')

                self.logger.INFO("Status counted successfully")

                return data

        except Exception as e:
            self.logger.ERROR(f"Error in totalStatus: {e}")
            return None

    def meanDateProcess(self, df, numberProcess: str = None):
        try:

            """
            Metodo para calcular a média de dias entre a data de ajuizamento e a data do ultimo movimento
            """

            self.logger.INFO("Starting meanDateProcess")

            df = self.dataframe.to_datetime(df, ["dataAjuizamento", "dataMovimentacao"])

            df_ultima_mov = df.groupby('numeroProcesso')['dataMovimentacao'].max().reset_index()

            df = df.merge(df_ultima_mov, on='numeroProcesso', suffixes=('', '_ultima'))

            # Contar o número de movimentações por processo
            num_movimentacoes = df.groupby('numeroProcesso')['dataMovimentacao'].count().reset_index()
            num_movimentacoes.rename(columns={'dataMovimentacao': 'numMovimentacoes'}, inplace=True)

            # Juntar com o DataFrame original
            df = df.merge(num_movimentacoes, on='numeroProcesso')

            # Calcular o tempo total de tramitação (diferença entre a última movimentação e o ajuizamento)
            df['tempoTotalTramitacao'] = df['dataMovimentacao_ultima'] - df['dataAjuizamento']

            # Calcular o tempo médio entre movimentações
            df['tempoMedioMovimentacao'] = df['tempoTotalTramitacao'] / df['numMovimentacoes']

            # Remover duplicatas, pois o explode pode ter repetido processos
            df = df.drop_duplicates(subset=['numeroProcesso']).reset_index(drop=True)

            df['tempoTotalTramitacao'] = df['tempoTotalTramitacao'].dt.round("s")
            df['tempoMedioMovimentacao'] = df['tempoMedioMovimentacao'].dt.round("s")

            self.logger.INFO(f"retorno param: {numberProcess}")

            if numberProcess is not None and numberProcess != "":
                self.logger.INFO(f"Calculating mean by process number: {numberProcess}")
                df = df[df["numeroProcesso"] == numberProcess]

                self.logger.INFO("Mean calculated successfully")
                return df[['numeroProcesso', "dataAjuizamento", "numMovimentacoes", 'tempoTotalTramitacao', 'tempoMedioMovimentacao']]

            else:
                self.logger.INFO("Mean calculated successfully")
                return df[['numeroProcesso', "dataAjuizamento", "numMovimentacoes", 'tempoTotalTramitacao', 'tempoMedioMovimentacao']]

        except Exception as e:
            self.logger.ERROR(f"Error in meanDateProcess: {e}")
            return None

    def processNewAndCloset(self, df):
        try:

            """
            Metodo para calcular a quantidade de processos novos e encerrados por mes e ano
            df -> Dataframe do datajud apenas com a data de ajuizamento e a data do ultimo movimento e os status
            """

            self.logger.INFO("Starting processNewAndCloset")

            df = self.dataframe.to_datetime(df, ["dataAjuizamento", "dataUltimoMovimento"])

            anos = range(df["dataAjuizamento"].map(lambda x: x.year).min(), self.utils.getToday().year + 1)
            meses = range(1, 13)

            combinacoes = list(product(anos, meses))

            # Criar um DataFrame de Calendário

            calendario = self.dataframe.DataFrame({
                "ano": [ano for ano, mes in combinacoes],
                "mes": [mes for ano, mes in combinacoes]
            })

            df["status"] = df["movimento"].apply(lambda x: "Encerrado" if "Baixa Definitiva" in x or "Definitivo" in x else "Novo")

            df["mesAjuizamento"] = df["dataAjuizamento"].dt.month
            df["anoAjuizamento"] = df["dataAjuizamento"].dt.year
            df["mesUltimoMovimento"] = df["dataUltimoMovimento"].dt.month
            df["anoUltimoMovimento"] = df["dataUltimoMovimento"].dt.year

            novos = df[df["status"] != "Encerrado"].groupby(["anoAjuizamento", "mesAjuizamento"]).size().reset_index(name="Novos")
            

            encerrados = df[df["status"] == "Encerrado"].groupby(["anoUltimoMovimento", "mesUltimoMovimento"]).size().reset_index(name="Encerrados")

            resultadoNovos = self.dataframe.merge(
                calendario, 
                novos, 
                left_on=["ano", "mes"], 
                right_on=["anoAjuizamento", "mesAjuizamento"], 
                how="outer"
            )
            
            resultadoNovos = resultadoNovos.drop(
                columns=["anoAjuizamento", "mesAjuizamento"]
            )

            resultadoEncerrados = self.dataframe.merge(
                calendario, 
                encerrados, 
                left_on=["ano", "mes"], 
                right_on=["anoUltimoMovimento", "mesUltimoMovimento"], 
                how="outer"
            )
            
            resultadoEncerrados = resultadoEncerrados.drop(
                columns=["anoUltimoMovimento", "mesUltimoMovimento"]
            )

            resultadoFinal = self.dataframe.merge(
                resultadoNovos, 
                resultadoEncerrados, 
                left_on=["ano", "mes"], 
                right_on=["ano", "mes"], 
                how="outer"
            )
            
            resultadoFinal = resultadoFinal.fillna(0)
            

            self.logger.INFO("Process calculated successfully")

            return resultadoFinal

        except Exception as e:
            self.logger.ERROR(f"Error in processNewAndCloset: {e}")
            return None