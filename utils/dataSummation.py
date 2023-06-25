from utils.dataHandler import dataHandler

class dataSummation(dataHandler):
    def __init__(self, url=None, option=None):
        super().__init__(url)
        self.option = option
        self.content = []

    def handleInputData(self, row, col):
        cost = self.content[row][col]
        if self.option: 
            cost = cost.replace('.', '')
            cost = cost.replace(',', '.')
        else:
            cost = cost.replace(',', '')
        return cost

    def summation(self, partBegin, partEnd, inputCol, outputCol):
        partTotal, allTotal = 0, 0
        partNum, allNum = 0, 0
        setRow, setCol = partBegin, outputCol

        for row in range(partBegin, partEnd+1):
            cost = self.handleInputData(row, inputCol)
            if cost and '/' in cost:
                num = cost.split('/')
                partNum, allNum = float(num[0]), float(num[1])
            else:
                partNum = float(cost) if cost else 0.0
                allNum = float(cost) if cost else 0.0

            if '-' not in self.content[row][0]:
                self.content[setRow][setCol] = str(partTotal) if partTotal == allTotal else f'{partTotal}/{allTotal}'
                partTotal, allTotal = partNum, allNum
                setRow = row
            else:
                partTotal += partNum
                allTotal += allNum
        return

    def partSummation(self, partBegin, partEnd):
        for col in range(2, len(self.content[0]), 4):
            self.summation(partBegin, partEnd, col+1, col+2)
        return

    def handleDataSummation(self):
        for worksheet in self.workSheetList:
            self.content = worksheet.get_all_values()
            partBegin, partEnd = self.getPartRange(self.content, 'A')
            self.partSummation(partBegin, partEnd)

            partBegin, partEnd = self.getPartRange(self.content, 'B')
            self.partSummation(partBegin, partEnd)

            self.updateSheet(worksheet, self.content)
        return

    def getDataSummationResult(self):
        self.handleDataSummation()
        return