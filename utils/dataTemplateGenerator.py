from utils.dataHandler import dataHandler
from config.country import COUNTRY_INFO

class dataTemplateGenerator(dataHandler):
    def __init__(self, url=None, country=None):
        super().__init__(url)
        self.country = country
        self.content = []
        

    def getSheetData(self):
        countryName = self.country.replace(' ','')
        countryName = countryName.upper()
        currency = COUNTRY_INFO[countryName]['Currency']
        currencyCode = COUNTRY_INFO[countryName]['CurrencyCode']
        countryCode = COUNTRY_INFO[countryName]['CountryCode']
        return currency, currencyCode, countryCode
    
    def updateContent(self, currency, currencyCode, countryCode):
        self.content[3][1] = self.country
        self.content[6][1] = f'{currency} ({currencyCode})'
        self.content[5][1] = countryCode
        self.content[5][0] = 'Country Code'
        return

    def handleTemplateGenerator(self):
        for worksheet in self.workSheetList:
            self.content = worksheet.get_all_values()
            currency, currencyCode, countryCode = self.getSheetData()
            self.updateContent(currency, currencyCode, countryCode)
            self.updateSheet(worksheet, self.content)
        return

    def getTemplateGeneratorResult(self):
        self.handleTemplateGenerator()
        return