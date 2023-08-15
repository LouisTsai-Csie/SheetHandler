from utils.dataCheck import dataCheck
from utils.dataInput import dataInput
from utils.dataConversion import dataConversion
from utils.dataSummation import dataSummation
from utils.dataTemplateGenerator import dataTemplateGenerator
from config import option

class Helper:
    def __init__(self, url=None, function=None, data=None):
        self.option = option
        self.url = url
        self.function = function
        self.data = data
        self.handler = None
        self.responseMessage = ''

    def handleDataCorrection(self):
        option = False if self.data['option']=='Normal' else True
        area = 'GLOBAL' if self.data['area']=='Global' else 'TAIWAN'
        self.handler = dataCheck(self.url, area, option)
        result = self.handler.getDataCheckResult()
        self.responseMessage = result
        return
    
    def handleDataInputCost(self):
        option = False if self.data['option']=='Normal' else True
        area = 'GLOBAL' if self.data['area']=='Global' else 'TAIWAN'
        self.handler = dataInput(self.url, area, option)
        self.handler.getDataInputResult()
        return

    def handleDataOutputSum(self):
        option = False if self.data['option']=='Normal' else True
        self.handler = dataSummation(self.url, option)
        self.handler.getDataSummationResult()
        return

    def handleDataConversion(self):
        option = False if self.data['option']=='Normal' else True
        area = 'GLOBAL' if self.data['area']=='Global' else 'TAIWAN'
        self.handler = dataConversion(self.url, option, area)
        self.handler.getDataConversionResult()
        return
    
    def handleDataGeneration(self):
        country = self.data['country']
        self.handler = dataTemplateGenerator(self.url, country)
        self.handler.getTemplateGeneratorResult()
        return

    def getResult(self):
        if self.function==option.DATA_CORRECTION:
            self.handleDataCorrection()
        elif self.function==option.DATA_INPUT_COST:
            self.handleDataInputCost()
        elif self.function==option.DATA_OUTPUT_SUM: 
            self.handleDataOutputSum()
        elif self.function==option.DATA_CONVERSION:
            self.handleDataConversion()
        elif self.function==option.DATA_GENERATION:
            self.handleDataGeneration()
        return self.responseMessage
        

