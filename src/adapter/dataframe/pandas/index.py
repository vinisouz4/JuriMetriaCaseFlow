import pandas as pd
import numpy as np

from src.adapter.logging.logging import LoggerHandler

class PandasDataFrame():
    def __init__(self):
        self.logger = LoggerHandler("PandasDataFrame")

    def read_csv(self, path: str) -> pd.DataFrame:
        
        self.logger.INFO(f"Reading csv file from path: {path}")
        
        return pd.read_csv(path)
    
    def to_DataFrame(self, data: list) -> pd.DataFrame:
        
        self.logger.INFO(f"Converting data to DataFrame")
        
        return pd.DataFrame(data)
    
    def to_datetime(self, data, column: list) -> pd.DataFrame:
        try:
            self.logger.INFO(f"Converting column to datetime")

            for i in column:
                data[i] = pd.to_datetime(data[i], errors='coerce')

            self.logger.INFO(f"Column converted to datetime")
            
            return data
        except Exception as e:
            self.logger.ERROR(f"Error in to_datetime: {e}")
            return None
        
    
    def getPastDate(self, days: int, today) -> pd.Timestamp:
        try:

            """
            Parameters:
            days: int - Number of days to subtract from today
            today: pd.Timestamp - Current date
            """

            self.logger.INFO(f"Calculating timedelta of {days} days")

            day = pd.Timestamp(today - pd.Timedelta(days=days))

            self.logger.INFO(f"Timedelta calculated successfully")
            
            return day
        except Exception as e:
            self.logger.ERROR(f"Error in timedelta: {e}")
            return None
        
    def groupby(self, df, columns: list, agg: dict) -> pd.DataFrame:
        try:
            """
            Parameters:
            df: pd.DataFrame - DataFrame to group
            columns: list - List of columns to group by
            agg: dict - Dictionary with columns and aggregation functions
                - Model: {'column': 'agg_function'}
            """

            self.logger.INFO(f"Grouping data by columns: {columns}")

            data = df.groupby(columns).agg(agg).reset_index()

            self.logger.INFO("Data grouped successfully")
            
            return data
        except Exception as e:
            self.logger.ERROR(f"Error in groupby: {e}")
            return None
        
    def convertToFloat(self, value: str) -> float:
        try:
            self.logger.INFO(f"Converting value to float")

            if value is None or pd.isna(value) or value == "":
                return 0.0

            value = value.replace("R$", "").replace("\xa0", "")
            value = value.replace(".", "").replace(",", ".")

            self.logger.INFO(f"Value converted to float")

            return float(value)
        except Exception as e:
            self.logger.ERROR(f"Error in convertToFloat: {e}")
            return None