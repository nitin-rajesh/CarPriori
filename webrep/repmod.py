import os
import json

class repo:

    def __init__(self, dir) -> None:
        self.dir = dir
        pass

    def addParamToFile(self,fname,key,value):

        data = {}
        try:
            with open(self.dir + '/' + fname,mode='r') as f:
                data = json.load(f)

            data[key] = value

            print(data)

            with open(self.dir + '/' + fname,mode='w') as fp:
                json.dump(data,fp)

        except:
            print('Skipped img')

    def getData(self, fname):
        data = {}

        if not fname.startswith(self.dir):
            fname = self.dir + '/' + fname
            
        with open(fname,mode='r') as f:
            data = json.load(f)

        return data

    def traverseRep(self):
        files = []
        for dirname in os.listdir(self.dir):
            try:
                for filename in os.listdir(self.dir + '/' + dirname):
                    if filename.endswith('json'):
                        files.append(dirname + '/' + filename)
            except:
                print('Skipped')

        return files

        

        