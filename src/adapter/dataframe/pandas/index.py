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