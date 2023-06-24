from utils import auth

class dataHandler:
    def __init__(self, url=None):
        self.url = url
        self.sheet = auth.authenticate(url)
        self.sheetKeyWord  = 'CASE'
        self.workSheetList = self.getSheet(self.sheet)
        self.partEnd = 'END'
        self.partABegin = 'PART A'
        self.partBBegin = 'PART B'
        self.alphaList = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def getSheet(self, sheet):
        workSheets = list(sheet.worksheets())
        workSheetList = [workSheet for workSheet in workSheets if self.sheetKeyWord in workSheet.title.upper()]
        return workSheetList

    def getPartRange(self, content, type):
        beginIndex, endIndex = -1, -1
        flag = False
        part = self.partABegin if type=='A' else self.partBBegin
        for row in range(len(content)):
            if content[row][0] == part: flag = True
            if flag and content[row][0]=='1': beginIndex = row
            if flag and content[row][0]==self.partEnd: endIndex = row
            if endIndex>=0: break
        return beginIndex, endIndex
    
    def getSheetRange(self, worksheet):
        totalRow, totalCol = worksheet.row_count, worksheet.col_count
        start = 'A1'
        end = self.getCurrentPosition(totalRow, totalCol)
        return f'{start}:{end}'
    
    def getCurrentPosition(self, row, col):
        col += 1
        if col>=len(self.alphaList):
            return self.alphaList[col//26] + self.alphaList[col%26] + str(row) 
        return self.alphaList[col%26] + str(row)
    
    def updateSheet(self, worksheet, content):
        sheetRange = self.getSheetRange(worksheet)
        worksheet.update(sheetRange, content)
        return


    

    