from bs4 import BeautifulSoup
import requests
import os
import json
import shutil
import re
from webrep import repo

def getBrandName(brandurl):
    return brandurl.split('/')[-1][:-len('-cars-monthly-sales')]

def getEngine(brandurl, carname):
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

def getDimensions(brandurl, carname):
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

def initData():
    with open('car_brands.txt',mode='r') as f:

        for url in f.read().split('\n'):

            brandname = getBrandName(url)

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
                                carDict['Engine'] = getEngine(url,name)
                                carDict['Dimensions'] = getDimensions(url,name)

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

def getImages():
    base_url = 'https://www.v3cars.com'
    for company in os.listdir('CarPriori-dataset'):
        try:
            for car in os.listdir('CarPriori-dataset/' + company):
                try:
                    url = base_url + '/' + company + '-cars/' + car[:-5].replace(' ','-')
                    # print(url)
                    page = requests.get(url)

                    soup = BeautifulSoup(page.content, 'html.parser')

                    img_url = base_url + soup.find('div',{'class':'model-overview'}).find('img')['src']
                    print(img_url)

                    rp = repo('CarPriori-dataset/' + company)
                    rp.addParamToFile(fname=car,key='Image',value=img_url)

                    # image = requests.get(img_url, stream=True)
                    
                    # if image.status_code == 200:
                    #     fname = 'Car-images/'+car.split('.')[0]+'.'+img_url.split('.')[-1]
                    #     print(fname)
                    #     with open(fname,mode='wb') as fp:
                    #         shutil.copyfileobj(image.raw, fp)
                    #         print('Downloaded')
                    # else:
                    #     print('Image not retrieved')

                except:
                    print('Skipped')
        except:
                    print('Skipped')


def addPrices():
    base_url = 'https://www.v3cars.com'
    for company in os.listdir('CarPriori-dataset'):
        try:
            for car in os.listdir('CarPriori-dataset/' + company):
                try:
                    url = base_url + '/' + company + '-cars/' + car[:-5].replace(' ','-')
                    # print(url)
                    page = requests.get(url)

                    soup = BeautifulSoup(page.content, 'html.parser')

                    pricelist = soup.find('div',{'class':'dlab-tabs'})

                    print(car)

                    priceArr = []

                    for price in pricelist.find_all('div',{'class':'rightview'}):
                        try:
                            val = float(re.search('[0-9]+[.][0-9]+',price.text).group())
                            if 'lakh' in price.text:
                                val *= 100000
                            elif 'Cr' in price.text:
                                val *= 10000000
                            priceArr.append(int(val))
                        except:
                            continue

                    print(priceArr.sort())

                    rp = repo('CarPriori-dataset/' + company)
                    rp.addParamToFile(fname=car,key='Prices',value=priceArr)

                    
                    print('\n')

                except:
                    print('Skipped')
        except:
            print('Skipped')
                

def addCompany():
    for company in os.listdir('CarPriori-dataset'):
        try:
            for car in os.listdir('CarPriori-dataset/' + company):
                try:
                    rp = repo('CarPriori-dataset/' + company)
                    rp.addParamToFile(fname=car,key='Company',value=company)
                except:
                    pass
        except:
            pass
        
        

if __name__ == '__main__':
    addCompany()