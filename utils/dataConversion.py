from utils.dataHandler import dataHandler
from utils import auth
from config.template import TEMPLATE
from config.countryCode import COUNTRY_CODE
from config.countyCode import COUNTY_CODE
from config.transpose import TRANSPOSE_DATA_GL, TRANSPOSE_DATA_TW
from config.codebook import CODEBOOK
from config.link import MASTERDATA_TAIWAN, MASTERDATA_GLOBAL, MASTERDATA_TAIWAN_ALTERNATIVE, MASTERDATA_GLOBAL_ALTERNATIVE

class dataConversion(dataHandler):
    def __init__(self, url=None, option=None ,area=None):
        super().__init__(url)
        self.option = option
        self.area = area
        self.content = []
        self.partMasterList  = []
        self.totalMasterList = []
        self.partData  = {}
        self.totalData = {}

    ### Difference
    def handleBasicInfo(self, option):
        data = self.partData if option=='PART' else self.totalData
        country = self.content[3][1]
        country = country.upper()
        country = country.replace(' ', '')
        data['country'] = COUNTRY_CODE[country]
        ### Taiwan Case
        if self.area=='TAIWAN':
            county = self.content[4][1]
            county = county.upper()
            county = county.replace(' ', '')
            data['country'] = COUNTY_CODE[county]
        
        data['incomecase'] = self.content[1][1]
        incomeCaseName = ['','CASE1','CASE2','CASE3','CASE4','CASE5','CASE6', 'CASE7', 'CASE8']
        return incomeCaseName[int(self.content[1][1])]
    
    def handleMiscInfo(self, count, incomecase, option):
        data = self.partData if option=='PART' else self.totalData
        transposeData = TRANSPOSE_DATA_TW if self.area=='TAIWAN' else TRANSPOSE_DATA_GL
        data['familytype']   = transposeData[incomecase]['familytype'][count]
        data['incomegender'] = transposeData[incomecase]['incomegender'][count]
        data['case']         = transposeData[incomecase]['case'][count]
        return 
    
    def conversion(self, data, partBegin, partEnd, col ,type, option):
        codebook = CODEBOOK['PART A'] if type=='A' else CODEBOOK['PART B']
        programName = None
        for i in range(partBegin, partEnd):
            if '-' not in self.content[i][0]: 
                item = str(self.content[i][1]).upper().replace(' ', '')
                varName = codebook[item]
                programName = varName + '_prog'
                if '/' not in self.content[i][col+2]:
                    data[varName] = self.content[i][col+2]
                    if self.content[i][col] and float(self.content[i][col+2]):
                        data[programName] += str(self.content[i][col]+';')
                else:
                    partNum, totalNum = self.content[i][col+2].split('/')
                    num = partNum if option=='PART' else totalNum
                    data[varName] = num
                    if self.content[i][col] and float(num):
                        data[programName] += (str(self.content[i][col]) + ';')
            elif self.content[i][col]: data[programName] += (str(self.content[i][col]) + ';')
        return
    
    def handleMiscData(self, data, option):
        total = 0
        codebook = CODEBOOK['PART A'] if type=='A' else CODEBOOK['PART B']
        items = list(codebook.values())
        if option=='A':
            for item in items:
                if item=='earning': continue
                total += float(data[item])
            data['totalbenefit'] = total
        else:
            for item in items:
                total += float(data[item])
            data['totalexpense'] = total
        return

    def handlePartData(self):
        self.partData  = TEMPLATE.copy()
        self.partData['alternative']  = 0
        for count, col in enumerate(range(2, len(self.content[0]), 4)):
            incomecase = self.handleBasicInfo('PART')
            self.handleMiscInfo(count, incomecase, 'PART')
            
            partBegin, partEnd = self.getPartRange(self.content, 'A')
            self.conversion(self.partData, partBegin, partEnd, col, 'A', 'PART')

            partBegin, partEnd = self.getPartRange(self.content, 'B')
            self.conversion(self.partData, partBegin, partEnd, col, 'B', 'PART')

            self.handleMiscData(self.partData, 'A')
            self.handleMiscData(self.partData, 'B')

            self.partMasterList.append(self.partData.copy())
        return
    
    def handleTotalData(self):
        self.totalData = TEMPLATE.copy()
        self.totalData['alternative'] = 1
        for count, col in enumerate(range(2, len(self.content[0]), 4)):
            incomecase = self.handleBasicInfo('TOTAL')
            self.handleMiscInfo(count, incomecase, 'TOTAL')

            partBegin, partEnd = self.getPartRange(self.content, 'A')
            self.conversion(self.totalData, partBegin, partEnd, col, 'A', 'TOTAL')

            partBegin, partEnd = self.getPartRange(self.content, 'B')
            self.conversion(self.totalData, partBegin, partEnd, col, 'B', 'TOTAL')

            self.handleMiscData(self.totalData, 'A')
            self.handleMiscData(self.totalData, 'B')

            self.totalMasterList.append(self.totalData.copy())
        return

    def workSheetConversion(self, worksheet):
        self.content   = worksheet.get_all_values()
        self.handlePartData()
        self.handleTotalData()    
        return

    def getStatSheet(self, url):
        sheet = auth.authenticate(url)
        worksheets = list(sheet.worksheets())
        for worksheet in worksheets:
            if 'STATISTICS' == worksheet.title.upper(): return worksheet
        return None

    def checkDuplicate(self, content, data):
        country, county, incomecase, familytype, incomegender, case, alternative = content[0], content[1], content[2], content[3], content[4], content[5], content[6]
        if str(data['country'])!=str(country):             return False
        if str(data['county'])!=str(county):               return False
        if str(data['incomecase'])!=str(incomecase):       return False
        if str(data['familytype'])!=str(familytype):       return False
        if str(data['incomegender'])!=str(incomegender):   return False
        if str(data['case'])!=str(case):                   return False
        if str(data['alternative'])!=str(alternative):     return False
        return True
    
    def updateStatSheet(self, sheet, masterList):
        content = sheet.get_all_values()
        title = ['country', 'county', 'incomecase', 'familytype', 'incomegender', 'case', 'alternative', 'earning', 'iliving', 'inutrition', 'iCCare', 'iCBenefit', 'ifertility', 'ieducation', 'ihousing', 'imedical', 'iutility', 'itransport', 'isocsec', 'itax', 'iwork', 'iunempinsurance', 'iunempsub', 'iother', 'totalbenefit', 
                 'incometax', 'localtax', 'pension', 'healthinsurance', 'unempinsurance', 'othercontribution', 'ccarecost', 'schlcosts', 'healthcost', 'rent', 'utilitycost', 'foodcost', 'telecost', 'transportcost', 'othercosts', 'totalexpense', 'earning_prog', 'iliving_prog', 'inutrition_prog', 'iCCare_prog', 'iCBenefit_prog', 
                 'ifertility_prog', 'ieducation_prog', 'ihousing_prog', 'imedical_prog', 'iutility_prog', 'itransport_prog', 'isocsec_prog', 'itax_prog', 'iwork_prog', 'iunempinsurance_prog', 'iunempsub_prog', 'iother_prog', 'incometax_prog', 'localtax_prog', 'pension_prog', 'healthinsurance_prog', 'unempinsurance_prog', 'othercontribution_prog', 'ccarecost_prog', 'schlcosts_prog', 'healthcost_prog', 'rent_prog', 'utilitycost_prog', 'foodcost_prog', 'telecost_prog', 'transportcost_prog', 'othercosts_prog']
        newContent = []
        newContent.append(title)
        data = []
        for i in range(1, len(content)):
            flag = False
            for j in range(len(masterList)):
                if self.checkDuplicate(content[i], masterList[j]): flag = True
                if flag: break
            if not flag: data.append(content[i])
        for i in range(len(masterList)):
            data.append(list(masterList[i].values()))
        data.sort(key=lambda x: x[0])
        newContent.extend(data)
        self.updateSheet(sheet, newContent)
        return

    def handleDataCollect(self):
        masterDataSheet = MASTERDATA_GLOBAL if self.area=='GLOBAL' else MASTERDATA_TAIWAN
        statSheet = self.getStatSheet(masterDataSheet)
        self.updateStatSheet(statSheet, self.partMasterList)
        masterDataAlternativeSheet = MASTERDATA_GLOBAL_ALTERNATIVE if self.area=='GLOBAL' else MASTERDATA_TAIWAN_ALTERNATIVE
        statSheet = self.getStatSheet(masterDataAlternativeSheet)
        self.updateStatSheet(statSheet, self.totalMasterList)
        return

    def handleDataConversion(self):
        for worksheet in self.workSheetList:
            self.workSheetConversion(worksheet)
        self.handleDataCollect()
        return

    def getDataConversionResult(self):
        self.handleDataConversion()
        return