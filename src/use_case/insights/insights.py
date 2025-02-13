from src.adapter.logging.logging import LoggerHandler
from src.api.apiDataJud.getAPIDataJud import getDataJud
from src.use_case.filteredColumns.columnsCaseFlow.tableCase import columnsTableCase
from src.utils.utils import Utils





class Insights():
    def __init__(self, IDataFrame):
        self.dataframe = IDataFrame
        self.readDataJud = getDataJud()
        self.logger = LoggerHandler("Insights")
        self.utils = Utils()
    
    def totalProcess(self, df):
        try:
            self.logger.INFO("Started calculating total process")
            
            data = df[columnsTableCase]
            
            totalProcess = data.shape[0]
            
            self.logger.INFO(f"Total process: {totalProcess}")
            
            return totalProcess

        except Exception as e:
            self.logger.ERROR(f"Error in totalProcess: {e}")
            return None

    def totalValueCause(self, df):
        try:
            self.logger.INFO("Started calculating total value cause")

            data = df[columnsTableCase]

            totalValueCause = data["value_cause"].sum()

            self.logger.INFO(f"Total value cause: {totalValueCause}")

            return totalValueCause

        except Exception as e:
            self.logger.ERROR(f"Error in totalValueCause: {e}")
            return None

    def distributionData(self, df, dateColumn):
        try:

            """
            Método para calcular os processos distruibuídos nos ultimos 30 dias e nos ultimos 7 dias
            Considerando a coluna do DataFrame: distribution_date
            """

            self.logger.INFO("Started calculating distribution data")

            data = self.dataframe.to_datetime(df, [dateColumn])

            today = self.utils.getToday()

            # Definindo as datas de 30 e 7 dias atrás
            # lastSixtyDaysProcess = self.dataframe.getPastDate(60, today)
            lastThirtyDaysProcess = self.dataframe.getPastDate(30, today)
            lastSevenDaysProcess = self.dataframe.getPastDate(7, today)

            # Filtrando os processos distribuídos nos ultimos 30 dias
            thirtyDaysProcess = data[data[dateColumn] >= lastThirtyDaysProcess].shape[0]
            sevenDaysProcess = data[data[dateColumn] >= lastSevenDaysProcess].shape[0]

            self.logger.INFO(f"Total process distributed in the last 30 days: {thirtyDaysProcess} and in the last 7 days: {sevenDaysProcess}")
            
            return thirtyDaysProcess, sevenDaysProcess
        except Exception as e:
            self.logger.ERROR(f"Error in distributionData: {e}")
            return None
        
    def totalUf(self, df):
        try:
            self.logger.INFO("Started calculating total uf")

            df["uf_count"] = df["uf"]

            agg = {
                'uf_count': 'count',  # Conta a quantidade de ocorrências de cada UF
                'value_cause': 'sum'  # Soma dos valores da coluna Value_cause
            }

            groupbyData = self.dataframe.groupby(df, ['uf'], agg)



            # groupbyData["value_cause"] = groupbyData["value_cause"].apply(lambda x: f"{x:.2f}")

            groupbyData["latitude"], groupbyData["longitude"] = zip(*groupbyData["uf"].map(self.utils.getLatLong))

            groupbyData = groupbyData[groupbyData["latitude"].notna() & groupbyData["longitude"].notna()]

            orderGroupData = groupbyData.sort_values(by="uf_count", ascending=False)
            
            self.logger.INFO(f"Total uf: {orderGroupData}")
            
            return orderGroupData
        except Exception as e:
            self.logger.ERROR(f"Error in totalUf: {e}")
            return None