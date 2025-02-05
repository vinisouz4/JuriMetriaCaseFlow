from src.adapter.logging.logging import LoggerHandler
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud





class Insights():
    def __init__(self, IDataFrame):
        self.dataFrame = IDataFrame
        self.readDataJud = ReadDataJud()
        self.readCaseFlowData = ReadCaseFlowData(IDataFrame)
        self.logger = LoggerHandler("Insights")

    
        