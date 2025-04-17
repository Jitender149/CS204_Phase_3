class HDU:
    # If forwarding is not enabled
    def dataHazardStalling(self, pipeline_instructions):
        # Extracting all states
        decode_state = pipeline_instructions[-2]
        execute_state = pipeline_instructions[-3]
        memory_state = pipeline_instructions[-4]
        writeback_state = pipeline_instructions[-5]

        # Initializing variables
        countHazards = 0
        countStalls = 0
        isDataHazard = False
        to_from = {'to': -1, 'from': -1}  # tracks hazard source and destination stages

        # Instruction in decode stage has not been decoded yet 
        decode_state = pipeline_instructions[-2] # extracts current instruction in decode stage
        instruction = bin(int(decode_state.IR[2:],16))[2:] # converts instruction to binary
        instruction = (32-len(instruction)) * '0' + instruction # pads with leading zeros to make it 32 bits
        decode_opcode = int(instruction[25:32],2) # extracts opcode from instruction
        if(decode_opcode in [19, 103, 3]): # for I type only Rs1 is used
            decode_state.RS1 = int(instruction[12:17],2)
            decode_state.RS2 = -1
        else:
            decode_state.RS1 = int(instruction[12:17],2)
            decode_state.RS2 = int(instruction[7:12],2)
            
        # WB → ID Hazard Check
        if writeback_state.RD != -1 and writeback_state.RD != 0 and not writeback_state.stall and not decode_state.stall:
            if writeback_state.RD == decode_state.RS1 or writeback_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards += 1
                countStalls += 2  # Need to wait for WB to complete
                to_from = {'to': 3, 'from': 4}  # 4 is WB stage, 3 is ID stage
        # Checking dependency between execute state and decode state
        if execute_state.RD != -1 and execute_state.RD != 0 and not execute_state.stall and not decode_state.stall:
            if execute_state.RD == decode_state.RS1 or execute_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards += 1
                countStalls += 1
                to_from = {'to': 3, 'from': 2}       
        # Checking dependency between memory state and decode state
        if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall and not decode_state.stall:
            if memory_state.RD == decode_state.RS1 or memory_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards += 1
                if(countStalls == 0):
                    countStalls += 1
                to_from = {'to': 3, 'from': 1}
    
        return [isDataHazard, countHazards, countStalls, to_from]
    
    # If forwarding is enabled
    def dataHazardForwarding(self,pipeline_instructions):
        # Extracting all states
        decode_state = pipeline_instructions[-2]
        execute_state = pipeline_instructions[-3]
        memory_state = pipeline_instructions[-4]
        writeback_state = pipeline_instructions[-5]
        # print the states
        print("Decode State:", decode_state)
        print("Execute State:", execute_state)
        print("Memory State:", memory_state)
        print("Writeback State:", writeback_state)
        # Initializing variables   
        countHazards = 0  # count of hazards detected
        isStall = False  # whether stall is needed
        stallPos = 2  # Position to insert stall/bubble
        to_from = {'to': -1, 'from': -1}  # tracks hazard source and destination stages
        to_for = [""] * 5  # track forwarding path between pipline stages
        
        # Instruction in decode stage has not been decoded yet , so we need to decode it now
        instruction = bin(int(decode_state.IR[2:],16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction
        decode_opcode = int(instruction[25:32],2)
        if(decode_opcode in [19, 103, 3]): # for I type only Rs1 is used    
            decode_state.RS1 = int(instruction[12:17],2)
            decode_state.RS2 = -1
        else:
            decode_state.RS1 = int(instruction[12:17],2)  # for R type both Rs1 and Rs2 are used
            decode_state.RS2 = int(instruction[7:12],2)
        
        # Extracting opcodes of each state, means which instruction is being executed in each stage, so we need to get the opcode of each stage
        instruction = bin(int(execute_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        execute_opcode = int(instruction[25:32], 2)

        instruction = bin(int(memory_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        memory_opcode = int(instruction[25:32], 2)

        instruction = bin(int(writeback_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        writeback_opcode = int(instruction[25:32], 2)
        
        # M -> M forwarding
        # WB has load instruction and memory has store instruction, so we need to forward the data from mem to mem
        # The load instruction is writing to a register RD and store instruction is using the same register as it RS2 and both the stages are not stalled
        if writeback_opcode == 3 and memory_opcode == 35 and not writeback_state.stall and not memory_state.stall:
            if writeback_state.RD != -1 and writeback_state.RD != 0 and writeback_state.RD == memory_state.RS2:
                memory_state.registerData = writeback_state.registerData
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[1] = "forwarded from mem"
                
        # M -> E forwarding
        if writeback_state.RD != -1 and writeback_state.RD != 0 and not writeback_state.stall:
            # case 1 : forwarding to RS1
            if writeback_state.RD == execute_state.RS1 and not execute_state.stall:
                execute_state.RA = writeback_state.registerData
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[2] = "forwarded from mem"
            # case 2 : forwarding to RS2
            if writeback_state.RD == execute_state.RS2 and not execute_state.stall:
                if execute_opcode != 35: # not a store instruction , WHY?
                    execute_state.RB = writeback_state.registerData
                else:
                    execute_state.registerData = writeback_state.registerData
                
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[2] = "forwarded from mem"
        # Non store case: 
        # LW x1, 0(x2) # WB stage: Load value into x1
        # ADD x3,x4,x1, the value goes to the ALU's second input
        # Store case:
        # LW x1, 0(x2) 
        # SW x3, 0(x1), the values is used as th meory address for the store. so goes in registerData for memory operations 

        # E -> E forwarding
        if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall:   # check if mmory stage is writing to a valid register, ensures memory stage isnt stalled
            if memory_opcode == 3:  # load instruction
                if execute_opcode == 35:  # store instruciton
                    if execute_state.RS1 == memory_state.RD and not execute_state.stall:
                        countHazards = countHazards + 1
                        isStall = True  # stall beacuase we cant forward memory data immediately
                        stallPos = 0
                        to_from = {'to':2, 'from': 1}
                else:  # for non store case
                    if (execute_state.RS1 == memory_state.RD or execute_state.RS2 == memory_state.RD) and not execute_state.stall:  # check if either operand needs the loaded value
                        countHazards = countHazards + 1
                        isStall = True
                        stallPos = 0
                        to_from = {'to':2, 'from': 1}
                    
            else: # non load instruction
                if execute_state.RS1 == memory_state.RD and not execute_state.stall:  # if execute stage needs the value as first operand
                    execute_state.RA = memory_state.registerData  # forward the value to RA
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[2] = "forwarded from execute"

                if execute_state.RS2 == memory_state.RD and not execute_state.stall: # second operand forwarding
                    if execute_opcode != 35: # store
                        execute_state.RB = memory_state.registerData
                    else:
                        execute_state.registerData = memory_state.registerData
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[2] = "forwarded from execute"
        
        if (decode_opcode == 99 or decode_opcode == 103) and not decode_state.stall: # SB and jalr
            # M -> D forwarding
            if writeback_state.RD != -1 and writeback_state.RD != 0 and not writeback_state.stall:
                # we check writeback beacause it reperesents the most recent value of a register, if a value is being written back, its newest version of that register
                # this ensures that we get the most up to date version in our forwarding
                if writeback_state.RD == decode_state.RS1:  # if decode stage needs the value as first operand
                    decode_state.RA = writeback_state.registerData
                    decode_state.decode_forwarding_op1 = True
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[3] = "forwarded from mem"

                if writeback_state.RD == decode_state.RS2:  # if decode stage needs the value as second operand
                    decode_state.RB = writeback_state.registerData
                    decode_state.decode_forwarding_op2 = True
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[3] = "forwarded from mem"

            # E -> D fowarding
            # if we are not able to get the value from WB, we check memory stage (end of prev stage)
            if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall:
                if memory_opcode == 3 and (memory_state.RD == decode_state.RS1 or memory_state.RD == decode_state.RS2): # load
                    countHazards += 1
                    isStall = True
                    if stallPos > 1:
                        stallPos = 1
                        to_from = {'to': 3, 'from': 1}

                else:
                    if memory_state.RD == decode_state.RS1:
                        decode_state.RA = memory_state.registerData
                        decode_state.decode_forwarding_op1 = True
                        countHazards += 1
                        to_from = {'to': -1, 'from': -1}
                        to_for[3] = "forwarded from execute"

                    if memory_state.RD == decode_state.RS2:
                        decode_state.RB = memory_state.registerData
                        decode_state.decode_forwarding_op2 = True
                        countHazards += 1
                        to_from = {'to': -1, 'from': -1}
                        to_for[3] = "forwarded from execute"

            # If control instruction depends on the previous instruction
            if execute_state.RD != -1 and execute_state.RD != 0 and (execute_state.RD == decode_state.RS1 or execute_state.RD == decode_state.RS2) and not execute_state.stall:
                countHazards += 1
                isStall = True
                if stallPos > 1:
                    stallPos = 1
                    to_from = {'to': 3, 'from': 2}
                    
        to_from['from'] = to_for
        new_states = [writeback_state, memory_state, execute_state, decode_state, pipeline_instructions[-1]]
        return [countHazards, isStall, stallPos, new_states, to_from]
