import json
from turtle import clear
import pandas as pd
import numpy as np


def writeJson(data, fileName):
    with open(fileName, 'w') as f:
        json.dump(data, f)



def insertData(tag, pattern, response):
    # print(f'Pattern : {pattern}\nResponse : {response}')

    with open('demo.json') as file:
        final = json.load(file)

        try:

            temp = final['intent']

            if len(temp)<=0:
            
                myDict = {"tag": tag, "patterns": [], "responses": []}
                if type(pattern) == type(float('nan')):
                    return -1
                else:
                    myDict['patterns'].append(pattern)
                if type(response) == type(float('nan')):
                    return -1
                else:
                    myDict['responses'].append(response)

                data = final['intent']
                data.append(myDict)

                writeJson(final, "demo.json")
                return 'Data updated successfully'

            else:
                for i in range(len(temp)):
                    data = final['intent'][i]
                    if (('tag' in data.keys()) and (data['tag']==tag)):
                        if(pattern not in data['patterns']):
                            if type(pattern) == type(float('nan')):
                                return -1
                            else:
                                data['patterns'].append(pattern)
                            if type(response) == type(float('nan')):
                                return -1
                            else:
                                data['responses'].append(response)
                        
                        writeJson(final, "demo.json")
                        return 'Data updated successfully'

                    else:
                        myDict = {"tag": tag, "patterns": [], "responses": []}
                        if type(pattern) == type(float('nan')):
                            return -1
                        else:
                            myDict['patterns'].append(pattern)

                        if type(response) == type(float('nan')):
                            return -1
                        else:
                            myDict['responses'].append(response)

                        data = final['intent']
                        data.append(myDict)

                    writeJson(final, "demo.json")
                    return 'Data updated successfully'
                
            # return 'Data updated successfully'

        # temp.append(ls)
        # print(temp)
        except KeyError as e:
            print(f'Error occered')
        

def excelToJson(fileName):
    df = pd.read_excel(fileName, engine='odf')
    # df = df1.replace(np.nan, ' ', inplace=True)

    for i in df.index:
        a=insertData(df['Tags'][i], df['Patterns'][i], df['Response'][i])
        print(a)

# excelToJson('values.ods')