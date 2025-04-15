import json

filename = 'reg.txt'
dict1 = {}

fields = ['register', 'hex', 'binary', 'decimal']

with open(filename) as fh:
    array = []
    for line in fh:
        description = list(line.strip().split(None,4))
        # print(description)
        
        dict2 = {}
        i = 0
        while i < len(fields):
            dict2[fields[i]] = description[i]
            i = i + 1
        
        array.append(dict2)
    
    # print(array)
    filepath = '../frontend/src/components/reg.json'
    jsonFile = open(filepath,'w')
    json.dump(array,jsonFile,indent=4)
    jsonFile.close()
    

filename = 'data.txt'

fields = ['memory', 'hex', 'binary', 'decimal']
with open(filename) as fh:
    array = []
    for line in fh:
        description = list(line.strip().split(None,4))
        # print(description)
        
        dict2 = {}
        i = 0
        while i < len(fields):
            dict2[fields[i]] = description[i]
            i = i + 1
        
        array.append(dict2)
    
    # print(array)
    filepath = '../frontend/src/components/data.json'
    jsonFile = open(filepath,'w')
    json.dump(array,jsonFile,indent=4)
    jsonFile.close()
    
filename = 'cycle.txt'
filename2 = 'input.txt'
arr = []
with open(filename2) as fh:
    for line in fh:
        arr.append(line.strip('\n'))
        
# print(f"arr[0]: {arr[0]}")
fields = ['id','writeback','memory','execute','decode','fetch',"forwarding","value"]
with open(filename) as fh:
    array = []
    for line in fh:
        dataFields = line.split("  ")
        
        dict2 = {}
        i = 0
        while i < len(fields)-2:
            dict2[fields[i]] = dataFields[i]
            i = i + 1
        
        if(arr[0] == 'False' or (arr[0] == 'True' and arr[1] == 'False')):
            dict2[fields[i]] = '-1'
            dict2[fields[i+1]] = '-1'
        else:
            dataFields[i] = dataFields[i].replace("\'", "\"")
            # print(type(dataFields[i]))
            y = json.loads(dataFields[i])
            # print(y)
            j = 0
            val = '-1'
            for elt in y['from']:
                if(elt != ''):
                    val = elt
                    break
                else:
                    j = j + 1
            
            if(j == 5):
                j = -1
            dict2[fields[i]] = str(j)
            dict2[fields[i+1]] = val
            
        array.append(dict2)
        
    filepath = '../frontend/src/components/cycle.json'
    jsonFile = open(filepath,'w')
    json.dump(array,jsonFile,indent=4)
    jsonFile.close()
    
    
filename = 'stats.txt'
fields = ['stats', 'value']
with open(filename) as fh:
    array = []
    for line in fh:
        description = line.strip('\n').split(': ')
        
        dict2 = {}
        i = 0
        while i < len(fields):
            dict2[fields[i]] = description[i]
            i = i + 1
        
        array.append(dict2)
    
    # print(array)
    filepath = '../frontend/src/components/stats.json'
    jsonFile = open(filepath,'w')
    json.dump(array,jsonFile,indent=4)
    jsonFile.close()
    
        
        