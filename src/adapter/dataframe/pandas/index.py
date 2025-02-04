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