import pandas as pd
import numpy as np

from src.adapter.logging.logging import LoggerHandler

class PandasDataFrame():
    def __init__(self):
        self.logger = LoggerHandler("PandasDataFrame")

    def read_csv(self, path: str) -> pd.DataFrame:
        
        self.logger.INFO(f"Reading csv file from path: {path}")
        
        return pd.read_csv(path)
    
    def from_dict(self, data: dict) -> pd.DataFrame:
        
        self.logger.INFO(f"Converting data to DataFrame")
        
        return pd.DataFrame(data)
    
    def to_DataFrame(self, data: list) -> pd.DataFrame:
        
        self.logger.INFO(f"Converting data to DataFrame")
        
        return pd.DataFrame(data)
    
    def to_datetime(self, data, column: list) -> pd.DataFrame:
        try:
            self.logger.INFO(f"Converting column to datetime")

            for i in column:
                data[i] = pd.to_datetime(data[i], errors='coerce')

                if data[i].dt.tz is not None:
                    data[i] = data[i].dt.tz_convert(None)

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
            self.logger.INFO(f"Converting value to float: {value}")

            if value is None or pd.isna(value) or value == "":
                return 0.0

            value = value.replace("R$", "").replace("\xa0", "")
            value = value.replace(".", "").replace(",", ".")

            self.logger.INFO(f"Value converted to float")

            return float(value)
        except Exception as e:
            self.logger.ERROR(f"Error in convertToFloat: {e}")
            return None

    def removeSpecialCharacters(self, value: str) -> str:
        try:
            self.logger.INFO(f"Removing special characters from value: {value}")

            value = value.replace(".", "").replace("-", "")

            self.logger.INFO(f"Special characters removed")

            return value
        except Exception as e:
            self.logger.ERROR(f"Error in removeSpecialCharacters: {e}")
            return None
        
    def merge(self, df1, df2, left_on: list, right_on: list, how: str) -> pd.DataFrame:
        try:
            """
            Parameters:
            df1: pd.DataFrame - First DataFrame to merge
            df2: pd.DataFrame - Second DataFrame to merge
            on: str - Column to merge
            """

            self.logger.INFO(f"Merging dataframes")

            data = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)

            self.logger.INFO("Dataframes merged successfully")
            
            return data
        except Exception as e:
            self.logger.ERROR(f"Error in merge: {e}")
            return None
        
    def concat(self, df1, df2, axis) -> pd.DataFrame:
        try:
            """
            Parameters:
            df1: pd.DataFrame - First DataFrame to concat
            df2: pd.DataFrame - Second DataFrame to concat
            axis: int - Axis to concat
            """

            self.logger.INFO(f"Concatenating dataframes")

            data = pd.concat([df1, df2], axis=axis)

            self.logger.INFO("Dataframes concatenated successfully")
            
            return data
        except Exception as e:
            self.logger.ERROR(f"Error in concat: {e}")
            return None

    def json_normaliza(self, df, column, suffix = None, listDropColum: list = None):
        """
        Parameters:
        df: pd.DataFrame - DataFrame to normalize
        column: list - columns to normalize
        suffix: str - Suffix to add in columns
        listDropColum: list - List of columns to drop
        """
        try:
            self.logger.INFO(f"Normalizing json columns")

            if listDropColum is not None or suffix is not None:
                dfFinal = df.join(pd.json_normalize(df[column].explode()).add_suffix(suffix)).drop(columns=listDropColum)

            else:
                dfFinal = df.join(pd.json_normalize(df[column].explode()).add_suffix(suffix))

            self.logger.INFO("Json columns normalized successfully")
            
            return dfFinal
        except Exception as e:
            self.logger.ERROR(f"Error in json_normaliza: {e}")
            return None