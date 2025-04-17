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
    
# Convert stack_states.txt to stack_states.json
filename = 'stack_states.txt'
with open(filename) as fh:
    array = []
    current_cycle = None
    current_stack = []
    
    for line in fh:
        line = line.strip()
        if line.startswith('=== Cycle'):
            # Save previous cycle if exists
            if current_cycle is not None:
                array.append({
                    'cycle': current_cycle,
                    'stack': current_stack.copy()
                })
            
            # Start new cycle
            try:
                current_cycle = int(line.split(' ')[2])
            except (IndexError, ValueError):
                print(f"Warning: Could not parse cycle number from line: {line}")
                continue
            current_stack = []
        elif line.startswith('Stack Level'):
            try:
                # Parse stack entry
                parts = line.split(':')
                if len(parts) < 2:
                    print(f"Warning: Invalid stack level format: {line}")
                    continue
                    
                # Get instruction type
                next_line = next(fh).strip()
                if not next_line.startswith('Instruction Type:'):
                    print(f"Warning: Expected instruction type, got: {next_line}")
                    continue
                instruction_type = next_line.split(': ')[1]
                
                # Get return address
                next_line = next(fh).strip()
                if not next_line.startswith('Return Address:'):
                    print(f"Warning: Expected return address, got: {next_line}")
                    continue
                return_address = int(next_line.split(': ')[1], 16)
                
                # Get PC
                next_line = next(fh).strip()
                if not next_line.startswith('PC:'):
                    print(f"Warning: Expected PC, got: {next_line}")
                    continue
                pc = int(next_line.split(': ')[1], 16)
                
                current_stack.append({
                    'instruction_type': instruction_type,
                    'return_address': return_address,
                    'pc': pc
                })
            except (StopIteration, ValueError, IndexError) as e:
                print(f"Warning: Error parsing stack entry: {str(e)}")
                continue
    
    # Save last cycle
    if current_cycle is not None:
        array.append({
            'cycle': current_cycle,
            'stack': current_stack.copy()
        })
    
    filepath = '../frontend/src/components/stack_states.json'
    jsonFile = open(filepath, 'w')
    json.dump(array, jsonFile, indent=4)
    jsonFile.close()
    
        
        