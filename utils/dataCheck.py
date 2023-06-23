import re

from utils.dataHandler import dataHandler

class dataCheck(dataHandler):
    def __init__(self, url=None):
        super().__init__(url)
        self.errorMessage = ''
        self.content = []
    
    def regex(self, s):
        negative = '(^-?0\.[0-9]*[1-9]+[0-9]*$)|(^-?[1-9]+[0-9]*((\.[0-9]*[1-9]+[0-9]*$)|(\.[0-9]+)))|(^-?[1-9]+[0-9]*$)|(^0$){1}'
        if not re.match(negative, s): return False
        return True

    def regexChecker(self, s):
        if not len(s): return True
        s = s.replace(" ", "")
        s = s.replace("\n", "")
        slashCount = s.count("/")

        if not slashCount:
            if not self.regex(s): return False
        elif slashCount==1:
            s1, s2 = s.split('/')
            if not self.regex(s1) or not self.regex(s2): return False
        return True

    def check(self, partBegin, partEnd, inputCol):
        errorMessage = ''
        for row in range(partBegin, partEnd+1):
            cost = self.content[row][inputCol]
            result = self.regexChecker(cost)
            if not result: errorMessage += f'Invalid Format: {self.content[row][inputCol]} position: {self.getCurrentPosition(row+1, inputCol)}\n'
        return errorMessage
            

    def partCheck(self, partBegin, partEnd):
        result = ''
        for col in range(2, len(self.content[0]), 4):
            result += self.check(partBegin, partEnd, col+1)
        return result

    def handleWorksheetContent(self):
        result = ''
        ### Part A
        partBegin, partEnd = self.getPartRange(self.content, 'A')
        result += self.partCheck(partBegin, partEnd)

        ### Part B
        partBegin, partEnd = self.getPartRange(self.content, 'B')
        result += self.partCheck(partBegin, partEnd)
        return result

    def checkColumn(self, worksheet):
        self.content = worksheet.get_all_values()
        return True

    def handleDataCheck(self):
        for worksheet in self.workSheetList:
            self.errorMessage += f'<{worksheet.title}>\n\n'
            if not self.checkColumn(worksheet): continue

            result = self.handleWorksheetContent()
            # print(f'worksheet: {worksheet.title} result={result}')

            if not result: 
                self.errorMessage += 'Correctness Check Complete. No Invalid Format\n'
            else:
                self.errorMessage += result
            self.errorMessage += '=================\n\n'
        return
    
    def getDataCheckResult(self):
        self.handleDataCheck()
        return self.errorMessage