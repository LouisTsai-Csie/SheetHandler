from utils.dataHandler import dataHandler
from config.popularity import PEOPLEMULTIPLY_GL, PEOPLEMULTIPLY_TW

class dataInput(dataHandler):
    def __init__(self, url=None, area=None):
        super().__init__(url)
        self.area = area
        self.baseSheetNumber='6'
        self.baseSheet = self.getBaseSheet()
        self.baseCase = {
            'HEALTHCARECOST(MEDIAN/AVERAGE)':         0, # 9
            'UTILITYCOST(MEDIAN/AVERAGE)':            0, # 11
            'FOOD&GROCERIES(MEDIAN/AVERAGE)':         0, # 12
            'TELECOMMUNICATIONSCOST(MEDIAN/AVERAGE)': 0, # 13
            'TRANSPORTATIONCOST':                     0  # 14
        }
        self.content = []

    def getBaseSheet(self):
        workSheet = [workSheet for workSheet in self.workSheetList if self.baseSheetNumber in workSheet.title]
        return workSheet[0]
    
    def getBaseCase(self):
        content = self.baseSheet.get_all_values()
        partBegin, partEnd = self.getPartRange(content, 'B')
        tartgetItem = list(self.baseCase.keys())

        for i in range(partBegin, partEnd):
            itemName = str(content[i][1]).upper().replace(' ','')
            if itemName not in tartgetItem: continue
            self.baseCase[itemName] = float(content[i][3])
    
    def getIncomeCase(self):
        incomecase = int(self.content[1][1])
        incomeCaseName = ['', 'CASE1', 'CASE2', 'CASE3', 'CASE4', 'CASE5', 'CASE6', 'CASE7', 'CASE8', 'CASE9']
        return incomeCaseName[incomecase]

    def conversion(self, worksheet):
        self.content = worksheet.get_all_values()
        partBegin, partEnd = self.getPartRange(self.content, 'B')
        targetItem = list(self.baseCase.keys())
        incomeCase = self.getIncomeCase()
        multiply = PEOPLEMULTIPLY_TW if self.area=='TAIWAN' else PEOPLEMULTIPLY_GL
        for count, col in enumerate(range(2, len(self.content[0]), 4)):
            for i in range(partBegin, partEnd):
                itemName = self.content[i][1].upper().replace(' ', '')
                if itemName not in targetItem: continue
                multiType = 'origin' if itemName == 'HEALTHCARECOST(MEDIAN/AVERAGE)' else 'equivalized'
                self.content[i][col+1] = self.baseCase[itemName] * multiply[incomeCase][multiType][count]
        return

    def handleDataInput(self):
        self.getBaseCase()
        for worksheet in self.workSheetList:
            self.conversion(worksheet)
            self.updateSheet(worksheet, self.content)
        return

    def getDataInputResult(self):
        self.handleDataInput()
        return
    