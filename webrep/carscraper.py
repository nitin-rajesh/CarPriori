from bs4 import BeautifulSoup
import requests
import os
import json

class carscraper:
    def __init__(self) -> None:
        pass

    def getBrandName(self, brandurl):
        return brandurl.split('/')[-1][:-len('-cars-monthly-sales')]

    def getEngine(self, brandurl, carname):
        brandurl = brandurl[:-len('-monthly-sales')]
        brandurl += '/' + carname.lower().replace(' ','-') +'/engine-specifications'
        
        print(brandurl)

        page = requests.get(brandurl)

        data = {}

        soup = BeautifulSoup(page.content, 'html.parser')
        specs = soup.find('div',{'id':'engine-spec'})
        
        spec_names = specs.find_all('div',{'class':'leftview'})
        spec_values = specs.find_all('div',{'class':'rightview'})
        
        for spec_name, spec_val in zip(spec_names, spec_values):
            # print(spec_name.text,':',spec_val.text)
            data[spec_name.text] = spec_val.text

        # print(data)
        return data

    def getDimensions(self, brandurl, carname):
        brandurl = brandurl[:-len('-monthly-sales')]
        brandurl += '/' + carname.lower().replace(' ','-') +'/dimensions'
        
        page = requests.get(brandurl)

        soup = BeautifulSoup(page.content, 'html.parser')

        data = {}

        specs = soup.find('table').find('tbody')

        labels = ['Length','Width','Height','Wheelbase']

        for label, tr in zip(labels,specs.find_all('tr')):
            val = tr.find('span',{'class','lenth-text'}).text
            # print(label,':',)
            data[label] = val

        # print(data)
        return data

    def updateDB(self):

        with open('car_brands.txt',mode='r') as f:
            for url in f.read().split('\n'):

                brandname = self.getBrandName(url)

                try:
                    os.mkdir(brandname)
                finally:
                    pass
                
                page = requests.get(url)

                soup = BeautifulSoup(page.content, 'html.parser')

                for table in soup.findAll('table'):

                    trs = table.find('tbody').findAll('tr')
                    for tr in trs:
                        carDict = {}
                        salesArr = []
                        for cells in tr.findAll('td'):

                            for cell in cells:
                                try:
                                    name = str(cell.find('a').text)
                                    # print(name,end=', \n')
                                    carDict['Car'] = name
                                    carDict['Engine'] = self.getEngine(url,name)
                                    carDict['Dimensions'] = self.getDimensions(url,name)

                                except:
                                    # print(cell, end=', ')
                                    salesArr.append(cell)

                        carDict['Sales'] = salesArr
                        print(carDict)
                        with open(brandname+'/'+carDict['Car']+'.json',mode='w') as fp:
                            try:
                                json.dump(carDict,fp)
                            except:
                                print(carDict['Car'],' skipped')