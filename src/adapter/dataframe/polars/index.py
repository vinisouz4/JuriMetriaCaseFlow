# import polars as pl
# import numpy as np

# from src.adapter.logging.logging import LoggerHandler

# class PolarsDataFrame():
#     def __init__(self):
#         self.logger = LoggerHandler("PolarsDataFrame")

#     def read_csv(self, path: str):
        
#         self.logger.INFO(f"Reading csv file from path: {path}")
        
#         return pl.read_csv(path)