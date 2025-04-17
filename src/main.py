from processor import *
from state import *
from btb import *
from hdu import *
import json
import os

# Global lists to track program counter, hazards and control signals
pc_tmp = []
dataHazardPairs = []
controlHazardSignals = []

def evaluate(pipelineInstructions):
    # 1. Write Back Stage (WB)
    processor.writeBack(pipelineInstructions[0])
    # - Writes results back to registers
    # - Updates register values with computed results
    # - Final stage of pipeline

    # 2. Memory Access Stage (MEM)
    processor.memoryAccess(pipelineInstructions[1])
    # - Handles memory operations (load/store)
    # - Reads from or writes to data memory
    # - Fourth stage of pipeline

    # 3. Execute Stage (EX)
    processor.execute(pipelineInstructions[2])
    # - Performs ALU operations
    # - Handles arithmetic/logical operations
    # - Third stage of pipeline

    # 4. Decode Stage (ID)
    controlHazard, controlPC, enter, color = processor.decode(pipelineInstructions[3], btb)
    # - Decodes instruction
    # - Sets up control signals
    # - Detects control hazards (branches/jumps)
    # - Second stage of pipeline
    # Returns:
    # - controlHazard: if branch/jump detected
    # - controlPC: target address for branch/jump
    # - enter: if entering branch prediction
    # - color: branch prediction color

    # 5. Control Signal Handling
    if enter:
        controlHazardSignals.append(2)
    elif pipelineInstructions[2].stall and color !=0 and len(controlHazardSignals) > 0 and controlHazardSignals[-1] == 2:
        controlHazardSignals.append(controlHazardSignals[-1])
    else:
        controlHazardSignals.append(color)
    # - Tracks branch prediction states
    # - 2: entering branch prediction
    # - Maintains prediction history

    # 6. Fetch Stage (IF)
    processor.fetch(pipelineInstructions[4],btb)
    # - Fetches next instruction
    # - First stage of pipeline
    # - Uses BTB for branch prediction

    # 7. Update stack state after each cycle
    processor.update_stack_state()
    # - Records the current state of the call stack
    # - Adds it to stack_states list for later output

    # 8. Return Updated Pipeline State
    return [pipelineInstructions[1],pipelineInstructions[2],pipelineInstructions[3],pipelineInstructions[4]], controlHazard, controlPC
    # Returns:
    # - Updated pipeline instructions (excluding WB stage)
    # - Control hazard status
    # - Next PC value for branches
        

def main():
    global processor, btb, hdu
    
    file1="demofile.txt"
    knob_input=open("input.txt", "r")
    knobs=[]
    for line in knob_input:
        x=line.split()
        if x[0]=='True':
            if len(x)==1:
                knobs.append(True)
            else:
                knobs.append([True,x[1]]) # True with additional parameters
        
        else:
            if len(x)==1:
                knobs.append(False)
            else:
                knobs.append([False,x[1]]) # Fasle with additional parameters
                # for the last line of the input.txt file, ie which pipline register to print 
    knob_input.close()
    # Knobs
    pipelining_knob=knobs[0]  # knob1
    forwarding_knob=knobs[1]   # knob2
    print_registers_each_cycle=knobs[2]    # knob3
    print_pipeline_registers=knobs[3]   # knob4
    print_specific_pipeline_registers=knobs[4]  # knob5
    # Various Counts
    stalls_due_to_data_hazard = 0
    number_of_data_hazards = 0
    stalls_due_to_control_hazard = 0
    totalStalls = 0

    # initializing the classes
    processor = processor(file1)
    hdu=HDU()
    btb=BTB()

    # Signals
    PC = 0
    clock_cycles = 0
    prog_end = False

    if not pipelining_knob:
        # pipelining is disabled
        processor.pipeliningEnabled=False
        while True:

            curr_instruction=State(PC) # creating a new state object for the current instruction

            # FETCH STAGE
            processor.fetch(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1, -1, -1, curr_instruction.PC]) 
            # in non pipelined mode, only one instruction is active at a time and it is in the fetch stage at this point
            # and u understand that first -1 corresponds to WB, then MEM , then EX, then ID and then IF finally as in this order these enter the pipline cycle
            # DECODE STAGE
            processor.decode(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1, -1, curr_instruction.PC,-1])

            if processor.terminate:
                prog_end = True
                break
            
            processor.execute(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1,curr_instruction.PC,-1,-1])

            processor.memoryAccess(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1,curr_instruction.PC,-1,-1,-1])

            processor.writeBack(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([curr_instruction.PC,-1,-1,-1,-1])

            # Update stack state after each cycle in non-pipelined mode
            processor.update_stack_state()
            
            PC=processor.PC_next

    else:
        processor.pipeliningEnabled = True
        pipelineInstructions = [State(0) for x in range(5)] # create a list of 5 state objects
        for i in range(4):
            pipelineInstructions[i].stall = True # set the stall flag to true for all except the last one, Why only first 4? because the last one will be the current instruction
        '''
        The WB stage is left ready because it's the final stage
        It needs to be ready to complete any instructions that make it through the pipeline
        If WB was stalled, completed instructions couldn't write back
        '''
        while not prog_end:
            if not forwarding_knob: # non forwarding mode, ie only stalling for hazards
                
                dataHazard = hdu.dataHazardStalling(pipelineInstructions) # check for data hazards
                oldStates = pipelineInstructions # saving thr current pipline stages
                pipelineInstructions, controlHazard, controlPC = evaluate(pipelineInstructions) # evaluate the pipeline instructions...core logic of the pipelining 
                # But why we evaluate in reverse order?
                # print the results of evaluate
                print("Data Hazard:", dataHazard[0])
                print("Number of Data Hazards:", dataHazard[1])
                print("Number of Stalls:", dataHazard[2])
                print("To:", dataHazard[3]['to'])
                print("From:", dataHazard[3]['from'])
                tmp = []
                for i in range(5):
                    if oldStates[i].stall:
                        tmp.append(-1)  # mark stalled stage with -1
                    else:
                        tmp.append(oldStates[i].PC)  # record the PC of active stages
                pc_tmp.append(tmp)
                # this way we created a snapshot of pipline state at this clock cycle
                # -1 indicates stalled stages 
                # PC value indicated active instructions in each stage
                
                # Now we record the hazard information
                dataHazardPairs.append(dataHazard[3])
                # stores the hazard detection results

                # Now check branch prediction
                branch_taken = pipelineInstructions[3].branch_taken
                branch_pc = pipelineInstructions[3].PC_next
                # get the branch prediction from decode stage
                # we need whether the branch was taken or not
                # and the target address

                # Update PC
                PC += 4

                # Handle branch prediction
                if branch_taken and not dataHazard[0]:
                    PC = branch_pc
                # Handle control hazard                
                if controlHazard and not dataHazard[0]:
                    stalls_due_to_control_hazard += 1
                    PC = controlPC
                    pipelineInstructions.append(State(PC))
                    pipelineInstructions[-2].stall = True
                    # if control hazard (branch/jump) detected, increment control hazard stall counter and update the PC o target address
                    # Add new instruction state and stall the previous instructions
                    # eg: # Before:
                    # pipelineInstructions = [IF, ID, EX, MEM, WB]  # 5 stages
                    # After append:
                    # pipelineInstructions = [IF, ID, EX, MEM, WB, NEW]  # 6 stages
                    # NEW is the instruction at branch target
                    # When a branch is taken, we need to fetch the instruction at the target address
                    # The new state represents this target instruction
                    # It will flow through the pipeline stages
                    # Previous instruction is stalled to prevent incorrect execution

                if dataHazard[0]:
                    number_of_data_hazards += dataHazard[1]
                    stalls_due_to_data_hazard += dataHazard[2]
                    pipelineInstructions = pipelineInstructions[:2] + [State(0)] + oldStates[3:]
                    pipelineInstructions[2].stall = True
                    PC -= 4
                # if data hazard detected, update hazard and stall counter, insert bubble in pipeline
                # stall affected stage, and rewind PC to refetch instruction

                # if no control or data hazard, add new instruction at the end of pipeline
                if not controlHazard and not dataHazard[0]:
                    pipelineInstructions.append(State(PC))
                
                pipelineInstructions[-2].PC_next = PC # set next PC for instruction fetch stage

                prog_end = True
                for i in range(4):
                    x = pipelineInstructions[i]
                    if not x.stall:
                        prog_end = False
                        break
                # check if all pipline stages are stalled , if any stage active continue execution
                clock_cycles+=1
            else:
                dataHazard, ifStall, stallPos, pipelineInstructions, toFrom = hdu.dataHazardForwarding(pipelineInstructions)
                '''
                Returns:
                dataHazard: Number of hazards detected
                ifStall: Whether we need to stall
                stallPos: Which stage to stall
                pipelineInstructions: Updated pipeline state
                toFrom: Forwarding path information
                '''
                oldStates = pipelineInstructions  # save the old state,used for stall handling later
                pipelineInstructions, controlHazard, controlPC = evaluate(pipelineInstructions)
                # now execute one cycle of the pipeline
                '''
                Returns:
                pipelineInstructions: Updated pipeline state
                controlHazard: Whether control hazard detected
                controlPC: Target address for control hazard
                '''
                tmp = []
                for i in range(5):
                    if oldStates[i].stall:
                        tmp.append(-1)  # for stalled stages, record -1
                    else:
                        tmp.append(oldStates[i].PC)  # record the PC of active stages
                pc_tmp.append(tmp)
                # this way we created a snapshot of pipline state at this clock cycle
                dataHazardPairs.append(toFrom)
                # record forwarding path information        
                branch_taken = pipelineInstructions[3].branch_taken
                branch_pc = pipelineInstructions[3].PC_next
                # get the branch prediction from decode stage
                # we need whether the branch was taken or not
                # and the target address

                PC += 4 # increment PC for next instruction

                if branch_taken and not ifStall:
                    PC = branch_pc
                
                if controlHazard and not ifStall:
                    stalls_due_to_control_hazard += 1
                    PC = controlPC
                    pipelineInstructions.append(State(PC))
                    pipelineInstructions[-2].stall = True
                '''
                if a control hazard is detected and we need to stall, we add a new state at the end of the pipeline
                and stall the previous instruction
                '''
                # data hazard handling
                if ifStall:
                    stalls_due_to_data_hazard += 1

                    if stallPos == 0:
                        pipelineInstructions = pipelineInstructions[:1] + [State(0)] + oldStates[2:]
                        pipelineInstructions[1].stall = True
                        PC -= 4

                    elif stallPos == 1:
                        pipelineInstructions = pipelineInstructions[:2] + [State(0)] + oldStates[3:]
                        pipelineInstructions[2].stall = True
                        PC -= 4
                    '''
                    For stall at position 1:
                    Inserts bubble after second stage
                    Stalls third stage
                    Reverts PC increment
                    AND
                    For stall at position 0:
                    Inserts bubble after first stage
                    Stalls second stage
                    Reverts PC increment
                    '''
                if(ifStall):
                    number_of_data_hazards += dataHazard

                if not controlHazard and not ifStall:
                    pipelineInstructions.append(State(PC))
                '''
                If no hazards:
                Adds new instruction to pipeline
                Uses current PC value
                '''
                
                pipelineInstructions[-2].PC_next = PC

                for inst in pipelineInstructions:
                    inst.decode_forwarding_op1 = False
                    inst.decode_forwarding_op2 = False
                '''
                Resets forwarding flags for next cycle
                Ensures clean state for next hazard detection
                '''
                # check if all pipline stages are stalled , if any stage active continue execution
                prog_end = True
                for i in range(4):
                    x = pipelineInstructions[i] 
                    if not x.stall:
                        prog_end = False
                        break
                
                clock_cycles += 1

            # Print the register values after each clock cycle
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                print("\n")

            # Print specific pipeline registers
            if print_specific_pipeline_registers[0]:
                for inst in pipelineInstructions:
                    if inst.PC/4 == int(print_specific_pipeline_registers[1], 10):
                        if not print_registers_each_cycle:
                            print("CLOCK CYCLE:", clock_cycles)
                            print("Pipeline Registers:-")
                            print("Fetch # Decode =>", "Instruction:", pipelineInstructions[3].IR)
                            print("Decode # Execute => ", "Operand1: ", pipelineInstructions[2].RA, ", Operand2: ", pipelineInstructions[2].RB)
                            print("Execute # Memory => ", "Data: ", pipelineInstructions[1].RY)
                            print("Memory # WriteBack => ", "Data: ", pipelineInstructions[0].RY)
                            print("\n")

            # Print pipeline registers
            elif print_pipeline_registers:
                if not print_registers_each_cycle:
                    print("CLOCK CYCLE:", clock_cycles)
                    print("Pipeline Registers:-")
                    print("Fetch # Decode =>", "Instruction:", pipelineInstructions[3].IR)
                    print("Decode # Execute => ", "Operand1: ", pipelineInstructions[2].RA, ", Operand2: ", pipelineInstructions[2].RB)
                    print("Execute # Memory => ", "Data: ", pipelineInstructions[1].RY)
                    print("Memory # WriteBack => ", "Data: ", pipelineInstructions[0].RY)
                    print("\n")
     
    pc_tmp.pop(-1)
    cycleFile = open("cycle.txt", "w")
    for i in range(len(pc_tmp)):
        cycleFile.write(str(i + 1) + "  ")
        for j in range(len(pc_tmp[i])):
            code = str(processor.riscvCode[pc_tmp[i][j]])
            cycleFile.write(code + "  ")
        if pipelining_knob:
            cycleFile.write(str(dataHazardPairs[i]))
        cycleFile.write("\n")
    cycleFile.close()

    totalStalls = stalls_due_to_control_hazard + stalls_due_to_data_hazard
    processor.writeDataMemory()
    # Printing the stats at the end of the simulation
    statsFile = open("stats.txt", "w")
    # Stats
    stats = [''] * 12
    stats[0] = "Number of clock cycles: " + str(clock_cycles) + "\n"
    stats[1] = "Number of instructions executed: " + str(processor.Total_instructions) + "\n"
    stats[2] = "CPI: " + str(clock_cycles / processor.Total_instructions) + "\n"
    stats[3] = "Number of data transfer (load & store) instructions executed: " + str(processor.memory_instructions) + "\n"
    stats[4] = "Number of ALU instructions executed: " + str(processor.ALU_instructions) + "\n"
    stats[5] = "Number of control instructions executed: " + str(processor.control_instructions) + "\n"
    stats[6] = "Number of stalls: " + str(totalStalls) + "\n"
    stats[7] = "Number of data hazards: " + str(number_of_data_hazards) + "\n"
    stats[8] = "Number of control hazards: "
    if processor.pipeliningEnabled:
        stats[8] += str(processor.control_instructions) + "\n"
    else:
        stats[8] += "0\n"
    stats[9] = "Number of branch mispredictions: " + str(processor.branch_misprediction) + "\n"
    stats[10] = "Number of stalls due to data hazards: " + str(stalls_due_to_data_hazard) + "\n"
    stats[11] = "Number of stalls due to control hazards: " + str(stalls_due_to_control_hazard) + "\n"

    statsFile.writelines(stats)
    statsFile.close()

    # Save branch prediction data
    branch_prediction_file = open("branch_prediction.txt", "w")
    branch_prediction_data = []
    
    # Calculate branch prediction accuracy
    total_branches = processor.control_instructions
    correct_predictions = total_branches - processor.branch_misprediction
    accuracy = (correct_predictions / total_branches * 100) if total_branches > 0 else 0
    
    # Prepare branch prediction data
    branch_prediction_data.append("Branch Prediction Statistics\n")
    branch_prediction_data.append("==========================\n")
    branch_prediction_data.append(f"Total branches executed: {total_branches}\n")
    branch_prediction_data.append(f"Correct predictions: {correct_predictions}\n")
    branch_prediction_data.append(f"Branch mispredictions: {processor.branch_misprediction}\n")
    branch_prediction_data.append(f"Branch prediction accuracy: {accuracy:.2f}%\n")
    branch_prediction_data.append(f"Branch prediction table size: {len(btb.table)}\n")
    
    # Add detailed branch prediction information
    branch_prediction_data.append("\nDetailed Branch Prediction Information\n")
    branch_prediction_data.append("==================================\n")
    for pred in processor.branch_prediction_details:
        branch_prediction_data.append(f"PC: 0x{pred['pc']:08x}\n")
        branch_prediction_data.append(f"Instruction: {pred['instruction']}\n")
        branch_prediction_data.append(f"Prediction: {pred['prediction']}\n")
        branch_prediction_data.append(f"Actual: {pred['actual']}\n")
        branch_prediction_data.append(f"Target Address: 0x{pred['target']:08x}\n")
        branch_prediction_data.append(f"Misprediction: {'Yes' if pred['misprediction'] else 'No'}\n")
        branch_prediction_data.append("-" * 50 + "\n")
    
    # Write to file
    branch_prediction_file.writelines(branch_prediction_data)
    branch_prediction_file.close()
    
    # Print branch prediction data to terminal
    print("\nBranch Prediction Statistics")
    print("==========================")
    print(f"Total branches executed: {total_branches}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Branch mispredictions: {processor.branch_misprediction}")
    print(f"Branch prediction accuracy: {accuracy:.2f}%")
    print(f"Branch prediction table size: {len(btb.table)}")
    
    print("\nDetailed Branch Prediction Information")
    print("==================================")
    for pred in processor.branch_prediction_details:
        print(f"PC: 0x{pred['pc']:08x}")
        print(f"Instruction: {pred['instruction']}")
        print(f"Prediction: {pred['prediction']}")
        print(f"Actual: {pred['actual']}")
        print(f"Target Address: 0x{pred['target']:08x}")
        print(f"Misprediction: {'Yes' if pred['misprediction'] else 'No'}")
        print("-" * 50)
    
    print("\nBranch prediction data saved to branch_prediction.txt")

    # After processing all instructions
    # Save stack states to a JSON file
    print("\nSaving stack states to JSON file...")
    print(f"Total stack states collected: {len(processor.stack_states)}")
    print(f"Sample stack state: {processor.stack_states[0] if processor.stack_states else 'No states collected'}")
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'src', 'Components', 'stack_states.json')
    with open(frontend_path, 'w') as f:
        json.dump(processor.stack_states, f)
    print(f"Stack states saved to: {frontend_path}")

if __name__ == '__main__':
    main()