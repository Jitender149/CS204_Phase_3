# from collections import defaultdict
# from btb import *
# from utility import *
# import os

# class processor:
#     def __init__(self, file1):
#         self.dataMemory = defaultdict(lambda: '00') # initialising data memory
#         # we made datamemory using dafultdict and 00 represent a zero byte in hex and this doesnt raises the key error (IMP)
#         self.instructionMemory = defaultdict(lambda: '00') # initialising instruction memory
#         self.registers = ['0x00000000' for i in range(32)] # initialising registers
#         self.registers[2]='0x7FFFFFF0' # sp
#         self.registers[3]='0x10000000' # gp
#         self.loadProgramMemory(file1) # read demofile.txt file to load our data and intruction memory
#         self.pipeliningEnabled = False # knob for pipelining
#         self.PC_next = 0 # Next PC address
#         self.PC_offset = 0 # PC offset
#         self.return_address = -1 # return address
#         self.terminate = False # flag to terminate the program
#         # Control Signals
#         self.registerWrite=False 
#         self.MuxB_select=False # control the second ALU input, when false uses register value, else use immediate value
#         self.MuxY_select=0 # control the write back data source, when 0 uses ALU result, when 1 uses memory data, when 2 uses PC+4
#         self.mem_write=False # control the write enable of data memory
#         self.mem_read=False # control the read enable of data memory
#         self.MuxMA_select=False # control the address source, when false uses ALU result, else uses PC+4
#         self.MuxPC_select=False # control the PC source, when false uses PC+4, else uses return address
#         self.MuxINC_select=False # control the PC increment source, when false uses PC+4, else uses PC offset
#         self.numBytes=0 # number of bytes to read/write from/to memory
#         # Counts
#         self.Total_instructions=0 # Total number of instructions executed
#         self.ALU_instructions=0 # Total number of ALU instructions executed
#         self.memory_instructions=0  # Total number of memory instructions executed
#         self.control_instructions=0 # Total number of control instructions executed
#         self.branch_misprediction=0 # Total number of branch mispredictions
#         # ALU : add, sub, mul, div, rem, and, or, xor, sll, srl, sra, slt, lt, gt
#         # Memory : lb, lh, lw, sb, sh, sw
#         # Control : jalr, jal, beq, bne, blt, bge, bltu, bgeu...so on
#         self.allStall=False # control global pipline stalling, when true, all stages are stalled, when false, pipeline is free to run
#         self.riscvCode = defaultdict(lambda: -1) # dictionary to store the riscv code
#         # Stack tracking
#         self.call_stack = []  # List to store return addresses
#         self.stack_states = []  # List to store stack state at each cycle

#     def reset(self, *args):
#         if len(args) > 0:
#             state = args[0]
#             state.MuxINC_select = False
#             state.MuxPC_select = False
#             state.PC_offset = 0
#             state.return_address = 0
#         else:
#             self.MuxINC_select = False
#             self.MuxPC_select = False
#             self.PC_offset = 0
#             self.return_address = 0
    
#     # Function to populate the instruction & data memory using the demofile.txt file    
#     def loadProgramMemory(self, file1):
#         try:
#             fp = open(file1, 'r')
#             flag = True
#             for line in fp:
#                 tmp = line.split()
#                 if len(tmp) == 2:
#                     address, instruction = tmp[0], tmp[1]
#                     if(instruction == '$'):
#                         flag = False
#                         continue
#                     # till flag is true, we are loading the instruction memory
#                     if(flag):   # little endian format
#                         idx = int(address[2:], 16) # convert hex address to integer
#                         self.instructionMemory[idx] = instruction[8:10]  # byte 3
#                         self.instructionMemory[idx+1] = instruction[6:8]  # byte 2
#                         self.instructionMemory[idx+2] = instruction[4:6]  # byte 1
#                         self.instructionMemory[idx+3] = instruction[2:4]  # byte 0
#                     else:  # flag is false, we are loading the data memory
#                         idx = int(address[2:], 16) # convert hex address to integer 
#                         instruction = '0x' + (10 - len(instruction))*'0' + instruction[2:] # convert instruction to hex
#                         self.dataMemory[idx] = instruction[8:10] # byte 3
#                         self.dataMemory[idx+1] = instruction[6:8] # byte 2
#                         self.dataMemory[idx+2] = instruction[4:6] # byte 1
#                         self.dataMemory[idx+3] = instruction[2:4] # byte 0
#         except:
#             print(f"Error: Unable to open {file1} file.\n")
#             exit(1)

#     # Function to print the contents of the data memory in data.txt file and register values in reg.txt file
#     def writeDataMemory(self):
#         try:
#             fp = open('data.txt', 'w')
#             output = []
#             for i in range(int('10000000', 16), int('10007ffd', 16), 4):
#                 tmp = self.dataMemory[i + 3] + self.dataMemory[i + 2] + self.dataMemory[i + 1] + self.dataMemory[i]
#                 output.append(hex(i).upper() + ' 0x' + tmp.upper() + ' ' + bin(int(tmp, 16))[2:] + ' ' + str(nint(tmp, 16)) + '\n')
#             fp.writelines(output)
#             fp.close()
#         except:
#             print("Error: Unable to open data.txt file for writing.\n")
#             exit(1)

#         try:
#             fp = open('reg.txt', 'w')
#             output = []
#             for i in range(32):
#                 output.append('x' + str(i) + ' ' + self.registers[i].upper() + ' ' + bin(int(self.registers[i], 16))[2:] + ' ' + str(nint(self.registers[i], 16)) + '\n')
#             fp.writelines(output)
#             fp.close()
#         except:
#             print("Error: Unable to open reg.txt file for writing.\n")
#             exit()

#     # Fetch
#     def fetch(self, state, *args): # variable length argument list,used for passing the BTB object
#         if state.stall == True: # This prevents processing the instruction if the pipeline is stalled
#             return
#         state.IR = '0x' + self.instructionMemory[state.PC + 3] + self.instructionMemory[state.PC + 2] + self.instructionMemory[state.PC + 1] + self.instructionMemory[state.PC]
#         # fetching the instruction from the instruction memory using the PC address
#         if self.allStall: # check if entire pipeline is stalled
#             state.stall=True # if so, mark current instruction as stalled
#             return

#         if not self.pipeliningEnabled: # if pipelining is disabled, return as no need of branch prediction in non pipelined mode
#             return
#         # Branch Prediction
#         btb=args[0] # BTB object is passed as an argument
#         if btb.find(state.PC):
#             state.branch_taken=btb.predict(state.PC)
#             if state.branch_taken:
#                 state.PC_next=btb.next_add(state.PC)
#             else:
#                 state.PC_next= state.PC + 4


#     # Function to update PC (instruction address generator)
#     def IAG(self, state):
#         if(state.MuxPC_select==False):
#             self.PC_next = state.return_address
#         else:
#             if(state.MuxINC_select==False):
#                 self.PC_next += 4
#             else:
#                 self.PC_next += state.PC_offset


#     # Decode
#     def decode(self, state, *args):
#         code = ''
#         if state.stall == True:
#             return False, 0, False, 0 # whether a control hazard is detected, number of stalls, whether a branch is taken, number of branches
        
#         if state.IR == '0x00000000':
#             self.terminate = True
#             state.stall = True
#             self.allStall = True
#             return False, 0, False, 0
        
#         self.Total_instructions += 1

#         for i in range(15):
#             state.ALU_OP[i] = False
#         # converting the instruction to binary format
#         instruction = bin(int(state.IR[2:], 16))[2:]
#         instruction = (32-len(instruction)) * '0' + instruction

#         # Opcode and func3
#         opcode = instruction[25:32]
#         func3 = int(instruction[17:20], 2)

#         # R Format
#         if(opcode == '0110011'):
#             state.generateControlSignals(True, False, 0, False, False, False, True, False, 4)
#             # For R-type instructions, the operation is always performed on the full width of the register, which is 32 bits (4 bytes).
#             state.RD = int(instruction[20:25], 2) # here 2 is the base argument
#             state.RS1 = int(instruction[12:17], 2)
#             state.RS2 = int(instruction[7:12], 2)
#             func7 = int(instruction[0:7], 2)

#             # ADD/SUB/MUL
#             if(func3 == 0x0):
#                 # ADD Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[0] = True
#                     code = 'ADD x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 # SUB Instruction
#                 elif(func7 == 0x20):
#                     state.ALU_OP[1] = True
#                     code = 'SUB x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 # MUL Instruction
#                 elif(func7 == 0x01):
#                     state.ALU_OP[3] = True
#                     code = 'MUL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Error: Unknown instruction")
#                     exit(1)
#             # AND
#             elif(func3 == 0x7):
#                 # AND Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[10] = True
#                     code = 'AND x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Error: Unknown instruction")
#                     exit(1)
#             # OR/REM
#             elif(func3 == 0x6):
#                 # OR Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[9] = True
#                     code = 'OR x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 # REM Instruction
#                 elif(func7 == 0x01):
#                     state.ALU_OP[4] = True
#                     code = 'REM x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Unknown Instruction")
#                     exit(1)
#             # SLL
#             elif(func3 == 0x1):
#                 # SLL Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[6] = True
#                     code = 'SLL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Error: Unknown instruction")
#                     exit(1)
#             # SLT
#             elif(func3 == 0x2):
#                 # SLT Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[11] = True;
#                     code = 'SLT x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Error: Unknown instruction")
#                     exit(1)
#             # SRL/SRA
#             elif(func3 == 0x5):
#                 # SRL Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[8] = True
#                     code = 'SRL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 # SRA Instruction
#                 elif(func7 == 0x20):
#                     state.ALU_OP[7] = True
#                     code = 'SRA x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Error: Unknown instruction")
#                     exit(1)
#             # XOR/DIV
#             elif(func3 == 0x4):
#                 # XOR Instruction
#                 if(func7 == 0x00):
#                     state.ALU_OP[5] = True
#                     code = 'XOR x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 # DIV Instruction
#                 elif(func7 == 0x01):
#                     state.ALU_OP[2] = True
#                     code = 'DIV x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
#                 else:
#                     print("Unknown instruction")
#                     exit(1)
#             else:
#                 print("Unknown instruction")

#             state.RA = nint(self.registers[state.RS1][2:], 16) # [2:] is used to remove the '0x' prefix and 16 is the base argument
#             state.RB = nint(self.registers[state.RS2][2:], 16)
#             # we got the operands for the ALU operation above
#             self.ALU_instructions += 1 # increment the ALU instructions count
            
#         # I Format
#         elif(opcode == '0010011' or opcode == '0000011' or opcode == '1100111'):
#             state.RD = int(instruction[20:25],2)
#             state.RS1 = int(instruction[12:17],2)
#             state.Imm = int(instruction[0:12],2)
            
#             if(state.Imm > 2047):
#                 state.Imm -= 4096 # sign extension
                
#             # LB/LH/LW
#             if(opcode == '0000011'):
#                 state.ALU_OP[0] = True
#                 # LB Instruction
#                 if(func3 == 0x0):
#                     state.generateControlSignals(True,True,1,True,False,False,True,False,1)  # as loading byte, we need to read 1 byte from the memory
#                     code = 'LB x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#                 # LH Instruction
#                 elif(func3 == 0x1):
#                     state.generateControlSignals(True,True,1,True,False,False,True,False,2)
#                     code = 'LH x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#                 # LW Instruction
#                 elif(func3 == 0x2):
#                     state.generateControlSignals(True,True,1,True,False,False,True,False,4)  # as loading word, we need to read 4 bytes from the memory
#                     code = 'LW x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#                 else:
#                     print("Unknown instruction")
#                     exit(1)
            
#                 state.RA = int(self.registers[state.RS1][2:], 16)  # refer to the updated_data&control_path to understand this better
#                 self.memory_instructions += 1
            
#             # ADDI/ANDI/ORI/XORI/SLLI/SRLI
#             elif(opcode == '0010011'):
#                 state.generateControlSignals(True,True,0,False,False,False,True,False,4)
#                 # even though the immediate is 12 bits, we are using 32 bits for the ALU operation as the immediate is sign extended to 32 bits
#                 # The 4 (last argument) is for numBytes, which tells the processor that the operation (and any data movement, if relevant) is on a 4-byte (32-bit) word.
#                 # ADDI Instruction
#                 if(func3 == 0x0):
#                     state.ALU_OP[0] = True
#                     code = 'ADDI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 # ANDI Instruction
#                 elif(func3 == 0x7):
#                     state.ALU_OP[10] = True
#                     code = 'ANDI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 # ORI Instruction
#                 elif(func3 == 0x6):
#                     state.ALU_OP[9] = True
#                     code = 'ORI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 # XORI Instruction
#                 elif(func3 == 0x4):
#                     state.ALU_OP[5] = True
#                     code = 'XORI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 # SLLI Instruction
#                 elif(func3 == 0x1):
#                     state.ALU_OP[6] = True
#                     code = 'SLLI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 # SRLI Instruction
#                 elif(func3 == 0x5):
#                     state.ALU_OP[8] = True
#                     code = 'SRLI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 else:
#                     print("Unknown instruction")
#                 state.RA = nint(self.registers[state.RS1][2:], 16) # refer as above
#                 self.ALU_instructions += 1
            
#             # JALR
#             elif(opcode == '1100111'):
#                 print(f"\nExecuting JALR instruction at PC: 0x{state.PC:08x}")
#                 print(f"Target address: 0x{state.RA + state.Imm:08x}")
#                 print(f"Return address: 0x{state.PC + 4:08x}")
#                 state.generateControlSignals(True,False,2,False,False,False,False,True,4)
#                 # JALR Instruction
#                 if(func3 == 0x0):
#                     state.ALU_OP[0] = True
#                     code = 'JALR x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
#                 else:
#                     print("Unknown Error")
#                     exit(1)
#                 state.isbranch=1
#                 state.RA = nint(self.registers[state.RS1][2:], 16)  # load RS1 as the base address
#                 state.return_address = state.RA + state.Imm # return address is the base address + immediate
#                 self.return_address = state.RA + state.Imm # return address is the base address + immediate
#                 # Check if this is a return instruction (typically ra is in x1)
#                 # If we're jumping to an address that matches a return address on the stack, pop it
#                 if state.RS1 == 1:  # x1 is the return address register
#                     # Check if we're returning to an address on the stack
#                     for entry in self.call_stack:
#                         if entry['return_address'] == state.RA + state.Imm:
#                             # This is a return, so pop from the stack
#                             self.pop_stack()
#                             break
#                     # If not found on stack but using ra register, it might still be a return
#                     # so we can optionally pop here too if that's the desired behavior
#                 else:
#                     # This is a new call, push the return address
#                     self.push_stack(state.PC + 4, 'JALR', state.PC)

#                 self.MuxPC_select = False # select the return address as the PC source
#                 self.control_instructions += 1 # ofc this is a control instruction
#                 state.registerData = state.PC + 4
#                 # Push return address to stack
#                 self.push_stack(state.PC + 4, 'JALR', state.PC)
        
#         # S Format
#         elif(opcode == '0100011'):
#             state.RS1 = int(instruction[12:17],2)
#             state.RS2 = int(instruction[7:12],2)
#             state.Imm = int(instruction[0:7] + instruction[20:25],2)
#             state.Imm = ImmediateSign(state.Imm,12)    # utility function to sign extend the immediate
#             state.ALU_OP[0] = True
            
#             # SB Instruction
#             if(func3 == 0x0):
#                 state.generateControlSignals(False,True,1,False,True,False,True,False,1)
#                 code = 'SB x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#             # SH Instruction
#             elif(func3 == 0x1):
#                 state.generateControlSignals(False,True,1,False,True,False,True,False,2)
#                 code = 'SH x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#             # SW Instruction
#             elif(func3 == 0x2):                            
#                 state.generateControlSignals(False,True,1,False,True,False,True,False,4)
#                 code = 'SW x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
#             else:
#                 print("Unknown Error")
#                 exit(1)
            
#             state.RA = int(self.registers[state.RS1][2:], 16) # ALU's first operand
#             state.RB = int(self.registers[state.RS2][2:], 16) # ALU's second operand
#             state.registerData = state.RB # store the second operand in the register data
#             self.memory_instructions += 1
        
#         # B Format
#         elif(opcode == '1100011'):
#             print(f"\nExecuting branch instruction at PC: 0x{state.PC:08x}")
#             state.RS1 = int(instruction[12:17], 2)
#             state.RS2 = int(instruction[7:12], 2)
            
#             state.RA = nint(self.registers[state.RS1][2:], 16)
#             state.RB = nint(self.registers[state.RS2][2:], 16)
            
#             state.Imm = int(instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24],2)
#             state.Imm = ImmediateSign(state.Imm,12)
#             state.Imm *= 2   # as 1 bit shifted already in the instruction
#             # BEQ Instruction
#             if(func3 == 0x0):
#                 print(f"BEQ instruction: x{state.RS1} (0x{state.RA:08x}) == x{state.RS2} (0x{state.RB:08x})")
#                 print(f"Branch target: 0x{state.PC + state.Imm:08x}")
#                 state.ALU_OP[12] = True
#                 code = 'BEQ x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
#                 # Push return address to stack if branch is taken
#                 if state.RA == state.RB:
#                     self.push_stack(state.PC + 4, 'BEQ', state.PC)
#             # BNE Instruction
#             elif(func3 == 0x1):
#                 print(f"BNE instruction: x{state.RS1} (0x{state.RA:08x}) != x{state.RS2} (0x{state.RB:08x})")
#                 print(f"Branch target: 0x{state.PC + state.Imm:08x}")
#                 state.ALU_OP[13] = True
#                 code = 'BNE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
#                 # Push return address to stack if branch is taken
#                 if state.RA != state.RB:
#                     self.push_stack(state.PC + 4, 'BNE', state.PC)
#             # BLT Instruction
#             elif(func3 == 0x4):
#                 print(f"BLT instruction: x{state.RS1} (0x{state.RA:08x}) < x{state.RS2} (0x{state.RB:08x})")
#                 print(f"Branch target: 0x{state.PC + state.Imm:08x}")
#                 state.ALU_OP[11] = True
#                 code = 'BLT x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
#                 # Push return address to stack if branch is taken
#                 if state.RA < state.RB:
#                     self.push_stack(state.PC + 4, 'BLT', state.PC)
#             # BGE Instruction
#             elif(func3 == 0x5):
#                 print(f"BGE instruction: x{state.RS1} (0x{state.RA:08x}) >= x{state.RS2} (0x{state.RB:08x})")
#                 print(f"Branch target: 0x{state.PC + state.Imm:08x}")
#                 state.ALU_OP[14] = True
#                 code = 'BGE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
#                 # Push return address to stack if branch is taken
#                 if state.RA >= state.RB:
#                     self.push_stack(state.PC + 4, 'BGE', state.PC)
#             else:
#                 print("Unknown Error")
#                 exit(1)
#             state.isbranch=2
#             state.generateControlSignals(False,False,0,False,False,False,True,False,0)
#             self.control_instructions += 1
            
#         # U Format
#         elif(opcode == '0010111' or opcode == '0110111'):
#             state.RD = int(instruction[20:25],2)
#             state.Imm = int(instruction[0:20],2)
#             state.Imm = ImmediateSign(state.Imm,20)
#             # AUIPC Instruction
#             if(opcode == '0010111'):
#                 code = 'AUIPC x' + str(state.RD) + ', ' + str(state.Imm)
#                 state.ALU_OP[0] = True
#                 state.RA = state.PC
#                 state.Imm = state.Imm << 12
#             # LUI Instruction
#             else:
#                 code = 'LUI x' + str(state.RD) + ', ' + str(state.Imm)
#                 state.ALU_OP[6] = True
#                 state.RA = state.Imm
#                 state.Imm = 12
            
#             state.generateControlSignals(True,True,0,False,False,False,True,False,0)
#             self.ALU_instructions += 1
        
#         # J Format
#         elif(opcode == '1101111'):
#             print(f"\nExecuting JAL instruction at PC: 0x{state.PC:08x}")
#             # JAL Instruction
#             state.RD = int(instruction[20:25],2)
#             state.Imm = int(instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11],2)
#             state.Imm =  ImmediateSign(state.Imm,20)
#             state.Imm *= 2
#             print(f"Target address: 0x{state.PC + state.Imm:08x}")
#             print(f"Return address: 0x{state.PC + 4:08x}")
#             state.ALU_OP[12] = True
#             code = 'JAL x' + str(state.RD) + ', ' + str(state.Imm)
#             state.RA = 0
#             state.RB = 0
#             state.isbranch=1
#             state.generateControlSignals(True,False,2,False,False,False,True,True,0)
#             self.control_instructions += 1
#             state.registerData = state.PC + 4 # return address and this will be written to the destination register
#             # Push return address to stack - JAL always jumps
#             self.push_stack(state.PC + 4, 'JAL', state.PC)
        
#         else:
#             print("Unknown Instruction")
#             exit(1)
        
#         self.riscvCode[state.PC] = code  # store the instruction in the riscvCode dictionary

#         if self.pipeliningEnabled:
#             enter = False # initializes a flag to track whether we need to enter a new branch into BTB 
#             if state.isbranch == 0:
#                 return False, 0, False, 0  # if the current instruction is not a branch, return early with Fasle: No branch misprediction, 0: No actual PC update, False: No new BTB entry needed, 0: No special handling needed
#             else:
#                 self.execute(state)  # if pipelining is enabled, execute the instruction
#                 self.PC_next = state.PC 
#                 self.IAG(state)  # calls IAG to calculate next PC, IAG is used to calculate the next PC
#                 actual_pc = self.PC_next

#                 btb = args[0]  # get BTB from the argument list and this is used for branch prediction
#                 if btb.find(state.PC) and actual_pc != state.PC_next: # if the branch was in BTB and prediction was wrong then increment the branch misprediction count
#                     self.branch_misprediction += 1 

#                 if not btb.find(state.PC): # if the branch is not in BTB, we need to add it to the BTB
#                     # copy various control signals to the state
#                     state.MucINC_select = self.MuxINC_select
#                     # pc_offset
#                     state.PC_offset = self.PC_offset
#                     # pc_select
#                     state.MuxPC_select = self.MuxPC_select
#                     # state_returnaddress
#                     state.return_address = self.return_address
#                     self.PC_next = state.PC
#                     self.IAG(state)
                    
#                     if(state.isbranch == 1):
#                         btb.enter(True, state.PC, self.PC_next) # whether branch was taken or not, and the current PC and the Target PC
#                     else:
#                         btb.enter(False, state.PC, self.PC_next)
                    
#                     self.reset()
#                     self.reset(state)
#                     enter = True # set the flag to True as we have entered a new branch into BTB

#                 else: # if the branch is already in BTB
#                     if(state.isbranch == 1):
#                         btb.enter(True, state.PC, self.PC_next) # update the BTB entry with the correct branch taken or not
#                     else:
#                         btb.enter(False, state.PC, self.PC_next)
#                 if actual_pc != state.PC_next:
#                     return True, actual_pc, enter, 1 # first value : whether there was a miprediction, Second value: Actual PCif misprediction occured, Third value: Whether new BTB entry was created, Fourth value: 1 if misprediction occured, 0 otherwise
#                 else:
#                     return False, 0, enter, 3


#     # Execute
#     def execute(self,state):
#         if (state.stall):
#             return
#         InA=state.RA
#         if state.MuxB_select:
#             InB=state.Imm
#         else:
#             InB=state.RB
            
#         state.MDR = nhex(state.registerData)
#         state.MDR = '0x' + ('0' * (10-len(state.MDR))) + state.MDR[2:]

#         for i in range(15):
#             if(state.ALU_OP[i]==1):
#                 if i==0:
#                     state.registerData=InA+InB
#                     break
#                 elif i==1:
#                     state.registerData=InA-InB
#                     break
#                 elif i==2:
#                     if(InB!=0):
#                         state.registerData=InA/InB
#                     break
#                 elif i==3:
#                     state.registerData=InA*InB
#                     break
#                 elif i==4:
#                     if(InB!=0):
#                         state.registerData=InA-InB
#                     break
#                 elif i==5:
#                     state.registerData=InA^InB
#                     break
#                 elif i==6:
#                     if (InB>=0):
#                         state.registerData=InA<<InB
#                     break
#                 elif i==7:
#                     #please write sra code here.
#                     break
#                 elif i==8:
#                     if (InB>=0):
#                         state.registerData=InA>>InB
#                     break
#                 elif i==9:
#                     state.registerData=InA|InB
#                     break
#                 elif i==10:
#                     state.registerData=InA&InB
#                     break
#                 # Branch Operations
#                 elif i==11:  # BLT
#                     if(InA<InB):
#                         state.MuxINC_select=True
#                         state.PC_offset = state.Imm
#                     self.PC_offset = state.Imm
#                     self.MuxINC_select = True
#                     break
#                 elif i==12:  # BEQ
#                     if(InA==InB):
#                         state.MuxINC_select=True
#                         state.PC_offset = state.Imm
#                     self.PC_offset = state.Imm
#                     self.MuxINC_select = True
#                     break
#                 elif i==13:  # BNE
#                     if(InA!=InB):
#                         state.MuxINC_select=True
#                         state.PC_offset = state.Imm
#                     self.PC_offset = state.Imm
#                     self.MuxINC_select = True
#                     break
#                 elif i==14:  # BGE
#                     if(InA>=InB):
#                         state.MuxINC_select=True
#                         state.PC_offset = state.Imm
#                     self.PC_offset = state.Imm
#                     self.MuxINC_select = True
#                     break
#                 else:
#                     break

#     # Memory Access
#     def memoryAccess(self,state):
#         if not self.pipeliningEnabled:  # if piplining is disabeled, we call IAG to calculate next PC 
#             self.IAG(state)

#         if state.stall: # if piplinine is stalled , return immediately without doing anything (USED FOR HANDLING HAZARDS)
#             return
        
#         # How to update RY?
#         if state.MuxY_select == 0: # if the MuxY_select is 0, then the RY is the register data
#             state.RY = state.registerData
#         elif state.MuxY_select == 1: # if the MuxY_select is 1, then the RY is the memory data
#             # Whether to access dataMemory?
#             if state.MuxMA_select == False: # if muxMA_select is false , set MAR to the computed address and this address comes form ALU calculations
#                 state.MAR = state.registerData

#                 # Memory Read (Load Instructions)
#                 if state.mem_read:
#                     if state.numBytes == 1:
#                         tmp = self.dataMemory[state.MAR]
#                         state.RY = nint(tmp,16,8) # convert to integer with 8 bit sign extension
#                     elif state.numBytes == 2:
#                         tmp = self.dataMemory[state.MAR + 1] + self.dataMemory[state.MAR] # read two bytes from memory and concatenate them, in little endian format
#                         state.RY = nint(tmp,16,16) 
#                     elif state.numBytes == 4:
#                         tmp = self.dataMemory[state.MAR + 3] + self.dataMemory[state.MAR + 2] + self.dataMemory[state.MAR + 1] + self.dataMemory[state.MAR]
#                         state.RY = nint(tmp,16,32)
#                     state.registerData = state.RY
                    
#                 # Memory Write (Store Instructions)
#                 elif state.mem_write:
#                     if state.numBytes == 1:
#                         self.dataMemory[state.MAR] = state.MDR[8:10]
#                     if state.numBytes == 2:
#                         self.dataMemory[state.MAR] = state.MDR[8:10]
#                         self.dataMemory[state.MAR + 1] = state.MDR[6:8]
#                     if state.numBytes == 4:
#                         self.dataMemory[state.MAR] = state.MDR[8:10]
#                         self.dataMemory[state.MAR + 1] = state.MDR[6:8]
#                         self.dataMemory[state.MAR + 2] = state.MDR[4:6]
#                         self.dataMemory[state.MAR + 3] = state.MDR[2:4]
#         elif state.MuxY_select == 2: # if the MuxY_select is 2, then the RY is the PC + 4
#             state.RY = state.PC + 4
        
#     # Write Back 
#     def writeBack(self, state):
#         if not state.stall: # if the pipeline is not stalled, then we can write back the result to the register
#             if state.registerWrite and state.RD != 0: # if the register write is enabled and the destination register is not 0
#                 tmp = nhex(state.RY) # convert the result to hexadecimal format
#                 tmp = '0x' + ('0' * (10 - len(tmp))) + tmp[2:] # add leading zeros to make it 10 characters long
#                 self.registers[state.RD] = tmp # write the result to the destination register

#     # def update_stack_state(self):
#     #     """
#     #     Records the current state of the call stack after each cycle.
#     #     This method is called at the end of each cycle to capture the stack state.
#     #     """
#     #     print(f"\nUpdating stack state at cycle {self.Total_instructions}")
#     #     print(f"Current call stack: {self.call_stack}")
#     #     current_stack = {
#     #         'cycle': self.Total_instructions,
#     #         'stack': [{'return_address': addr['return_address'], 
#     #                   'instruction_type': addr['instruction_type'],
#     #                   'pc': addr['pc']} for addr in self.call_stack]
#     #     }
#     #     print(f"New stack state: {current_stack}")
#     #     self.stack_states.append(current_stack)
        
#     #     # Print the current stack contents
#     #     print("\nCurrent Stack Contents:")
#     #     if not self.call_stack:
#     #         print("Stack is empty")
#     #     else:
#     #         for i, item in enumerate(self.call_stack):
#     #             print(f"Stack Level {i}:")
#     #             print(f"  Instruction Type: {item['instruction_type']}")
#     #             print(f"  Return Address: 0x{item['return_address']:08x}")
#     #             print(f"  PC: 0x{item['pc']:08x}")
#     def update_stack_state(self):
#         """
#         Records the current state of the call stack after each cycle.
#         This method is called at the end of each cycle to capture the stack state.
#         """
#         print(f"\nUpdating stack state at cycle {self.Total_instructions}")
#         print(f"Current call stack: {self.call_stack}")
#         current_stack = {
#             'cycle': self.Total_instructions,
#             'stack': [{'return_address': addr['return_address'], 
#                       'instruction_type': addr['instruction_type'],
#                       'pc': addr['pc']} for addr in self.call_stack]
#         }
#         print(f"New stack state: {current_stack}")
#         self.stack_states.append(current_stack)

#         # Print the current stack contents
#         print("\nCurrent Stack Contents:")
#         if not self.call_stack:
#             print("Stack is empty")
#         else:
#             for i, item in enumerate(self.call_stack):
#                 print(f"Stack Level {i}:")
#                 print(f"  Instruction Type: {item['instruction_type']}")
#                 print(f"  Return Address: 0x{item['return_address']:08x}")
#                 print(f"  PC: 0x{item['pc']:08x}")

#         # Write to stack_states.txt
#         try:
#             import os
#             current_dir = os.path.dirname(os.path.abspath(__file__))
#             file_path = os.path.join(current_dir, 'stack_states.txt')

#             with open(file_path, 'a') as f:  # Using 'a' for append mode
#                 f.write(f"\n=== Cycle {self.Total_instructions} ===\n")
#                 if not self.call_stack:
#                     f.write("Stack is empty\n")
#                 else:
#                     for i, item in enumerate(self.call_stack):
#                         f.write(f"Stack Level {i}:\n")
#                         f.write(f"  Instruction Type: {item['instruction_type']}\n")
#                         f.write(f"  Return Address: 0x{item['return_address']:08x}\n")
#                         f.write(f"  PC: 0x{item['pc']:08x}\n")
#                 f.write("-" * 50 + "\n")
            
#         except Exception as e:
#             print(f"Error writing to stack_states.txt: {str(e)}")

#     def push_stack(self, return_address, instruction_type, pc):
#         """
#         Pushes a return address onto the call stack when a branch or jump instruction is encountered.
        
#         Args:
#             return_address: The address to return to after the branch/jump
#             instruction_type: The type of instruction (JAL, JALR, BEQ, etc.)
#             pc: The program counter value of the branch/jump instruction
#         """
#         print(f"\nPushing to stack:")
#         print(f"Return Address: 0x{return_address:08x}")
#         print(f"Instruction Type: {instruction_type}")
#         print(f"PC: 0x{pc:08x}")
#         self.call_stack.append({
#             'return_address': return_address,
#             'instruction_type': instruction_type,
#             'pc': pc
#         })
#         print(f"Current stack size: {len(self.call_stack)}")

#     def pop_stack(self):
#         """
#         Pops a return address from the call stack when returning from a branch or jump.
        
#         Returns:
#             The return address entry that was popped, or None if the stack is empty
#         """
#         if self.call_stack:
#             popped_entry = self.call_stack.pop()
#             print(f"\nPopping from stack:")
#             print(f"Return Address: 0x{popped_entry['return_address']:08x}")
#             print(f"Instruction Type: {popped_entry['instruction_type']}")
#             print(f"PC: 0x{popped_entry['pc']:08x}")
#             return popped_entry
#         return None

#     def write_stack_states(self):
#         import os
#         print("\n=== Writing Stack States ===")
#         print(f"Number of stack states to write: {len(self.stack_states)}")
        
#         try:
#             # Get the absolute path to the src directory
#             current_dir = os.path.dirname(os.path.abspath(__file__))
#             file_path = os.path.join(current_dir, 'stack_states.txt')
            
#             print(f"\nFile Information:")
#             print(f"Current directory: {current_dir}")
#             print(f"Target file path: {file_path}")
#             print(f"Directory exists: {os.path.exists(current_dir)}")
#             print(f"File exists: {os.path.exists(file_path)}")
            
#             print("\nStack States Content:")
#             with open(file_path, 'w') as f:
#                 f.write("=== Current Stack States ===\n\n")
                
#                 # Write current stack contents
#                 f.write("Current Stack Contents:\n")
#                 if not self.call_stack:
#                     print("Stack is empty")
#                     f.write("Stack is empty\n")
#                 else:
#                     for i, item in enumerate(self.call_stack):
#                         stack_entry = f"Stack Level {i}:\n"
#                         stack_entry += f"  Instruction Type: {item['instruction_type']}\n"
#                         stack_entry += f"  Return Address: 0x{item['return_address']:08x}\n"
#                         stack_entry += f"  PC: 0x{item['pc']:08x}\n"
#                         print(stack_entry)
#                         f.write(stack_entry)
                
#                 f.write("\n" + "="*50 + "\n\n")
                
#                 # Write stack states history
#                 f.write("Stack States History:\n\n")
#                 for state in self.stack_states:
#                     f.write(f"Cycle {state['cycle']}:\n")
#                     if not state['stack']:
#                         f.write("  Stack is empty\n")
#                     else:
#                         for item in state['stack']:
#                             f.write(f"  Instruction Type: {item['instruction_type']}\n")
#                             f.write(f"  Return Address: 0x{item['return_address']:08x}\n")
#                             f.write(f"  PC: 0x{item['pc']:08x}\n")
#                             f.write("\n")
#                     f.write("-" * 50 + "\n")
            
#             print("\nSuccessfully wrote to file!")
            
#         except Exception as e:
#             print(f"\nError Details:")
#             print(f"Error type: {type(e).__name__}")
#             print(f"Error message: {str(e)}")
#             print(f"Current working directory: {os.getcwd()}")
#             print(f"Directory contents: {os.listdir('.')}")
#             print(f"Parent directory contents: {os.listdir('..')}")

from collections import defaultdict
from btb import *
from utility import *
import os

class processor:
    def __init__(self, file1):
        self.dataMemory = defaultdict(lambda: '00') # initialising data memory
        # we made datamemory using dafultdict and 00 represent a zero byte in hex and this doesnt raises the key error (IMP)
        self.instructionMemory = defaultdict(lambda: '00') # initialising instruction memory
        self.registers = ['0x00000000' for i in range(32)] # initialising registers
        self.registers[2]='0x7FFFFFF0' # sp
        self.registers[3]='0x10000000' # gp
        self.loadProgramMemory(file1) # read demofile.txt file to load our data and intruction memory
        self.pipeliningEnabled = False # knob for pipelining
        self.PC_next = 0 # Next PC address
        self.PC_offset = 0 # PC offset
        self.return_address = -1 # return address
        self.terminate = False # flag to terminate the program
        # Control Signals
        self.registerWrite=False 
        self.MuxB_select=False # control the second ALU input, when false uses register value, else use immediate value
        self.MuxY_select=0 # control the write back data source, when 0 uses ALU result, when 1 uses memory data, when 2 uses PC+4
        self.mem_write=False # control the write enable of data memory
        self.mem_read=False # control the read enable of data memory
        self.MuxMA_select=False # control the address source, when false uses ALU result, else uses PC+4
        self.MuxPC_select=False # control the PC source, when false uses PC+4, else uses return address
        self.MuxINC_select=False # control the PC increment source, when false uses PC+4, else uses PC offset
        self.numBytes=0 # number of bytes to read/write from/to memory
        # Counts
        self.Total_instructions=0 # Total number of instructions executed
        self.ALU_instructions=0 # Total number of ALU instructions executed
        self.memory_instructions=0  # Total number of memory instructions executed
        self.control_instructions=0 # Total number of control instructions executed
        self.branch_misprediction=0 # Total number of branch mispredictions
        # ALU : add, sub, mul, div, rem, and, or, xor, sll, srl, sra, slt, lt, gt
        # Memory : lb, lh, lw, sb, sh, sw
        # Control : jalr, jal, beq, bne, blt, bge, bltu, bgeu...so on
        self.allStall=False # control global pipline stalling, when true, all stages are stalled, when false, pipeline is free to run
        self.riscvCode = defaultdict(lambda: -1) # dictionary to store the riscv code
        # Stack tracking
        self.call_stack = []  # List to store return addresses
        self.stack_states = []  # List to store stack state at each cycle

    def reset(self, *args):
        if len(args) > 0:
            state = args[0]
            state.MuxINC_select = False
            state.MuxPC_select = False
            state.PC_offset = 0
            state.return_address = 0
        else:
            self.MuxINC_select = False
            self.MuxPC_select = False
            self.PC_offset = 0
            self.return_address = 0
    
    # Function to populate the instruction & data memory using the demofile.txt file    
    def loadProgramMemory(self, file1):
        try:
            fp = open(file1, 'r')
            flag = True
            for line in fp:
                tmp = line.split()
                if len(tmp) == 2:
                    address, instruction = tmp[0], tmp[1]
                    if(instruction == '$'):
                        flag = False
                        continue
                    # till flag is true, we are loading the instruction memory
                    if(flag):   # little endian format
                        idx = int(address[2:], 16) # convert hex address to integer
                        self.instructionMemory[idx] = instruction[8:10]  # byte 3
                        self.instructionMemory[idx+1] = instruction[6:8]  # byte 2
                        self.instructionMemory[idx+2] = instruction[4:6]  # byte 1
                        self.instructionMemory[idx+3] = instruction[2:4]  # byte 0
                    else:  # flag is false, we are loading the data memory
                        idx = int(address[2:], 16) # convert hex address to integer 
                        instruction = '0x' + (10 - len(instruction))*'0' + instruction[2:] # convert instruction to hex
                        self.dataMemory[idx] = instruction[8:10] # byte 3
                        self.dataMemory[idx+1] = instruction[6:8] # byte 2
                        self.dataMemory[idx+2] = instruction[4:6] # byte 1
                        self.dataMemory[idx+3] = instruction[2:4] # byte 0
        except:
            print(f"Error: Unable to open {file1} file.\n")
            exit(1)

    # Function to print the contents of the data memory in data.txt file and register values in reg.txt file
    def writeDataMemory(self):
        try:
            fp = open('data.txt', 'w')
            output = []
            for i in range(int('10000000', 16), int('10007ffd', 16), 4):
                tmp = self.dataMemory[i + 3] + self.dataMemory[i + 2] + self.dataMemory[i + 1] + self.dataMemory[i]
                output.append(hex(i).upper() + ' 0x' + tmp.upper() + ' ' + bin(int(tmp, 16))[2:] + ' ' + str(nint(tmp, 16)) + '\n')
            fp.writelines(output)
            fp.close()
        except:
            print("Error: Unable to open data.txt file for writing.\n")
            exit(1)

        try:
            fp = open('reg.txt', 'w')
            output = []
            for i in range(32):
                output.append('x' + str(i) + ' ' + self.registers[i].upper() + ' ' + bin(int(self.registers[i], 16))[2:] + ' ' + str(nint(self.registers[i], 16)) + '\n')
            fp.writelines(output)
            fp.close()
        except:
            print("Error: Unable to open reg.txt file for writing.\n")
            exit()

    # Fetch
    def fetch(self, state, *args): # variable length argument list,used for passing the BTB object
        if state.stall == True: # This prevents processing the instruction if the pipeline is stalled
            return
        state.IR = '0x' + self.instructionMemory[state.PC + 3] + self.instructionMemory[state.PC + 2] + self.instructionMemory[state.PC + 1] + self.instructionMemory[state.PC]
        # fetching the instruction from the instruction memory using the PC address
        if self.allStall: # check if entire pipeline is stalled
            state.stall=True # if so, mark current instruction as stalled
            return

        if not self.pipeliningEnabled: # if pipelining is disabled, return as no need of branch prediction in non pipelined mode
            return
        # Branch Prediction
        btb=args[0] # BTB object is passed as an argument
        if btb.find(state.PC):
            state.branch_taken=btb.predict(state.PC)
            if state.branch_taken:
                state.PC_next=btb.next_add(state.PC)
            else:
                state.PC_next= state.PC + 4


    # Function to update PC (instruction address generator)
    def IAG(self, state):
        if(state.MuxPC_select==False):
            self.PC_next = state.return_address
        else:
            if(state.MuxINC_select==False):
                self.PC_next += 4
            else:
                self.PC_next += state.PC_offset


    # Decode
    def decode(self, state, *args):
        code = ''
        if state.stall == True:
            return False, 0, False, 0 # whether a control hazard is detected, number of stalls, whether a branch is taken, number of branches
        
        if state.IR == '0x00000000':
            self.terminate = True
            state.stall = True
            self.allStall = True
            return False, 0, False, 0
        
        self.Total_instructions += 1

        for i in range(15):
            state.ALU_OP[i] = False
        # converting the instruction to binary format
        instruction = bin(int(state.IR[2:], 16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction

        # Opcode and func3
        opcode = instruction[25:32]
        func3 = int(instruction[17:20], 2)

        # R Format
        if(opcode == '0110011'):
            state.generateControlSignals(True, False, 0, False, False, False, True, False, 4)
            # For R-type instructions, the operation is always performed on the full width of the register, which is 32 bits (4 bytes).
            state.RD = int(instruction[20:25], 2) # here 2 is the base argument
            state.RS1 = int(instruction[12:17], 2)
            state.RS2 = int(instruction[7:12], 2)
            func7 = int(instruction[0:7], 2)

            # ADD/SUB/MUL
            if(func3 == 0x0):
                # ADD Instruction
                if(func7 == 0x00):
                    state.ALU_OP[0] = True
                    code = 'ADD x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                # SUB Instruction
                elif(func7 == 0x20):
                    state.ALU_OP[1] = True
                    code = 'SUB x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                # MUL Instruction
                elif(func7 == 0x01):
                    state.ALU_OP[3] = True
                    code = 'MUL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # AND
            elif(func3 == 0x7):
                # AND Instruction
                if(func7 == 0x00):
                    state.ALU_OP[10] = True
                    code = 'AND x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # OR/REM
            elif(func3 == 0x6):
                # OR Instruction
                if(func7 == 0x00):
                    state.ALU_OP[9] = True
                    code = 'OR x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                # REM Instruction
                elif(func7 == 0x01):
                    state.ALU_OP[4] = True
                    code = 'REM x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Unknown Instruction")
                    exit(1)
            # SLL
            elif(func3 == 0x1):
                # SLL Instruction
                if(func7 == 0x00):
                    state.ALU_OP[6] = True
                    code = 'SLL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # SLT
            elif(func3 == 0x2):
                # SLT Instruction
                if(func7 == 0x00):
                    state.ALU_OP[11] = True;
                    code = 'SLT x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # SRL/SRA
            elif(func3 == 0x5):
                # SRL Instruction
                if(func7 == 0x00):
                    state.ALU_OP[8] = True
                    code = 'SRL x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                # SRA Instruction
                elif(func7 == 0x20):
                    state.ALU_OP[7] = True
                    code = 'SRA x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # XOR/DIV
            elif(func3 == 0x4):
                # XOR Instruction
                if(func7 == 0x00):
                    state.ALU_OP[5] = True
                    code = 'XOR x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                # DIV Instruction
                elif(func7 == 0x01):
                    state.ALU_OP[2] = True
                    code = 'DIV x' + str(state.RD) + ', x' + str(state.RS1) + ', x' + str(state.RS2)
                else:
                    print("Unknown instruction")
                    exit(1)
            else:
                print("Unknown instruction")

            state.RA = nint(self.registers[state.RS1][2:], 16) # [2:] is used to remove the '0x' prefix and 16 is the base argument
            state.RB = nint(self.registers[state.RS2][2:], 16)
            # we got the operands for the ALU operation above
            self.ALU_instructions += 1 # increment the ALU instructions count
            
        # I Format
        elif(opcode == '0010011' or opcode == '0000011' or opcode == '1100111'):
            state.RD = int(instruction[20:25],2)
            state.RS1 = int(instruction[12:17],2)
            state.Imm = int(instruction[0:12],2)
            
            if(state.Imm > 2047):
                state.Imm -= 4096 # sign extension
                
            # LB/LH/LW
            if(opcode == '0000011'):
                state.ALU_OP[0] = True
                # LB Instruction
                if(func3 == 0x0):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,1)  # as loading byte, we need to read 1 byte from the memory
                    code = 'LB x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                # LH Instruction
                elif(func3 == 0x1):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,2)
                    code = 'LH x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                # LW Instruction
                elif(func3 == 0x2):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,4)  # as loading word, we need to read 4 bytes from the memory
                    code = 'LW x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                else:
                    print("Unknown instruction")
                    exit(1)
            
                state.RA = int(self.registers[state.RS1][2:], 16)  # refer to the updated_data&control_path to understand this better
                self.memory_instructions += 1
            
            # ADDI/ANDI/ORI/XORI/SLLI/SRLI
            elif(opcode == '0010011'):
                state.generateControlSignals(True,True,0,False,False,False,True,False,4)
                # even though the immediate is 12 bits, we are using 32 bits for the ALU operation as the immediate is sign extended to 32 bits
                # The 4 (last argument) is for numBytes, which tells the processor that the operation (and any data movement, if relevant) is on a 4-byte (32-bit) word.
                # ADDI Instruction
                if(func3 == 0x0):
                    state.ALU_OP[0] = True
                    code = 'ADDI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                # ANDI Instruction
                elif(func3 == 0x7):
                    state.ALU_OP[10] = True
                    code = 'ANDI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                # ORI Instruction
                elif(func3 == 0x6):
                    state.ALU_OP[9] = True
                    code = 'ORI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                # XORI Instruction
                elif(func3 == 0x4):
                    state.ALU_OP[5] = True
                    code = 'XORI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                # SLLI Instruction
                elif(func3 == 0x1):
                    state.ALU_OP[6] = True
                    code = 'SLLI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                # SRLI Instruction
                elif(func3 == 0x5):
                    state.ALU_OP[8] = True
                    code = 'SRLI x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                else:
                    print("Unknown instruction")
                state.RA = nint(self.registers[state.RS1][2:], 16) # refer as above
                self.ALU_instructions += 1
            
            # JALR
            elif(opcode == '1100111'):
                print(f"\nExecuting JALR instruction at PC: 0x{state.PC:08x}")
                print(f"Target address: 0x{state.RA + state.Imm:08x}")
                print(f"Return address: 0x{state.PC + 4:08x}")
                state.generateControlSignals(True,False,2,False,False,False,False,True,4)
                # JALR Instruction
                if(func3 == 0x0):
                    state.ALU_OP[0] = True
                    code = 'JALR x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                else:
                    print("Unknown Error")
                    exit(1)
                state.isbranch=1
                state.RA = nint(self.registers[state.RS1][2:], 16)  # load RS1 as the base address
                state.return_address = state.RA + state.Imm # return address is the base address + immediate
                self.return_address = state.RA + state.Imm # return address is the base address + immediate
                self.MuxPC_select = False # select the return address as the PC source
                self.control_instructions += 1 # ofc this is a control instruction
                state.registerData = state.PC + 4
                
                # Check if this is a return instruction (typically ra is in x1)
                # If we're jumping to an address that matches a return address on the stack, pop it
                is_return = False
                if state.RS1 == 1:  # x1 is the return address register
                    # Check if we're returning to an address on the stack
                    for entry in self.call_stack:
                        if entry['return_address'] == state.PC + 4:
                            # This is a return, so pop from the stack
                            self.pop_stack()
                            is_return = True
                            break
                
                # If not a return, push the return address to stack
                if not is_return:
                    self.push_stack(state.PC + 4, 'JALR', state.PC)
        
        # S Format
        elif(opcode == '0100011'):
            state.RS1 = int(instruction[12:17],2)
            state.RS2 = int(instruction[7:12],2)
            state.Imm = int(instruction[0:7] + instruction[20:25],2)
            state.Imm = ImmediateSign(state.Imm,12)    # utility function to sign extend the immediate
            state.ALU_OP[0] = True
            
            # SB Instruction
            if(func3 == 0x0):
                state.generateControlSignals(False,True,1,False,True,False,True,False,1)
                code = 'SB x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
            # SH Instruction
            elif(func3 == 0x1):
                state.generateControlSignals(False,True,1,False,True,False,True,False,2)
                code = 'SH x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
            # SW Instruction
            elif(func3 == 0x2):                            
                state.generateControlSignals(False,True,1,False,True,False,True,False,4)
                code = 'SW x' + str(state.RS2) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
            else:
                print("Unknown Error")
                exit(1)
            
            state.RA = int(self.registers[state.RS1][2:], 16) # ALU's first operand
            state.RB = int(self.registers[state.RS2][2:], 16) # ALU's second operand
            state.registerData = state.RB # store the second operand in the register data
            self.memory_instructions += 1
        
        # B Format
        elif(opcode == '1100011'):
            print(f"\nExecuting branch instruction at PC: 0x{state.PC:08x}")
            state.RS1 = int(instruction[12:17], 2)
            state.RS2 = int(instruction[7:12], 2)
            
            state.RA = nint(self.registers[state.RS1][2:], 16)
            state.RB = nint(self.registers[state.RS2][2:], 16)
            
            state.Imm = int(instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24],2)
            state.Imm = ImmediateSign(state.Imm,12)
            state.Imm *= 2   # as 1 bit shifted already in the instruction
            # BEQ Instruction
            if(func3 == 0x0):
                print(f"BEQ instruction: x{state.RS1} (0x{state.RA:08x}) == x{state.RS2} (0x{state.RB:08x})")
                print(f"Branch target: 0x{state.PC + state.Imm:08x}")
                state.ALU_OP[12] = True
                code = 'BEQ x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
                # Push return address to stack if branch is taken
                if state.RA == state.RB:
                    self.push_stack(state.PC + 4, 'BEQ', state.PC)
            # BNE Instruction
            elif(func3 == 0x1):
                print(f"BNE instruction: x{state.RS1} (0x{state.RA:08x}) != x{state.RS2} (0x{state.RB:08x})")
                print(f"Branch target: 0x{state.PC + state.Imm:08x}")
                state.ALU_OP[13] = True
                code = 'BNE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
                # Push return address to stack if branch is taken
                if state.RA != state.RB:
                    self.push_stack(state.PC + 4, 'BNE', state.PC)
            # BLT Instruction
            elif(func3 == 0x4):
                print(f"BLT instruction: x{state.RS1} (0x{state.RA:08x}) < x{state.RS2} (0x{state.RB:08x})")
                print(f"Branch target: 0x{state.PC + state.Imm:08x}")
                state.ALU_OP[11] = True
                code = 'BLT x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
                # Push return address to stack if branch is taken
                if state.RA < state.RB:
                    self.push_stack(state.PC + 4, 'BLT', state.PC)
            # BGE Instruction
            elif(func3 == 0x5):
                print(f"BGE instruction: x{state.RS1} (0x{state.RA:08x}) >= x{state.RS2} (0x{state.RB:08x})")
                print(f"Branch target: 0x{state.PC + state.Imm:08x}")
                state.ALU_OP[14] = True
                code = 'BGE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
                # Push return address to stack if branch is taken
                if state.RA >= state.RB:
                    self.push_stack(state.PC + 4, 'BGE', state.PC)
            else:
                print("Unknown Error")
                exit(1)
            state.isbranch=2
            state.generateControlSignals(False,False,0,False,False,False,True,False,0)
            self.control_instructions += 1
            
        # U Format
        elif(opcode == '0010111' or opcode == '0110111'):
            state.RD = int(instruction[20:25],2)
            state.Imm = int(instruction[0:20],2)
            state.Imm = ImmediateSign(state.Imm,20)
            # AUIPC Instruction
            if(opcode == '0010111'):
                code = 'AUIPC x' + str(state.RD) + ', ' + str(state.Imm)
                state.ALU_OP[0] = True
                state.RA = state.PC
                state.Imm = state.Imm << 12
            # LUI Instruction
            else:
                code = 'LUI x' + str(state.RD) + ', ' + str(state.Imm)
                state.ALU_OP[6] = True
                state.RA = state.Imm
                state.Imm = 12
            
            state.generateControlSignals(True,True,0,False,False,False,True,False,0)
            self.ALU_instructions += 1
        
        # J Format
        elif(opcode == '1101111'):
            print(f"\nExecuting JAL instruction at PC: 0x{state.PC:08x}")
            # JAL Instruction
            state.RD = int(instruction[20:25],2)
            state.Imm = int(instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11],2)
            state.Imm =  ImmediateSign(state.Imm,20)
            state.Imm *= 2
            print(f"Target address: 0x{state.PC + state.Imm:08x}")
            print(f"Return address: 0x{state.PC + 4:08x}")
            state.ALU_OP[12] = True
            code = 'JAL x' + str(state.RD) + ', ' + str(state.Imm)
            state.RA = 0
            state.RB = 0
            state.isbranch=1
            state.generateControlSignals(True,False,2,False,False,False,True,True,0)
            self.control_instructions += 1
            state.registerData = state.PC + 4 # return address and this will be written to the destination register
            # Push return address to stack - JAL always jumps
            self.push_stack(state.PC + 4, 'JAL', state.PC)
        
        else:
            print("Unknown Instruction")
            exit(1)
        
        self.riscvCode[state.PC] = code  # store the instruction in the riscvCode dictionary

        if self.pipeliningEnabled:
            enter = False # initializes a flag to track whether we need to enter a new branch into BTB 
            if state.isbranch == 0:
                return False, 0, False, 0  # if the current instruction is not a branch, return early with Fasle: No branch misprediction, 0: No actual PC update, False: No new BTB entry needed, 0: No special handling needed
            else:
                self.execute(state)  # if pipelining is enabled, execute the instruction
                self.PC_next = state.PC 
                self.IAG(state)  # calls IAG to calculate next PC, IAG is used to calculate the next PC
                actual_pc = self.PC_next

                btb = args[0]  # get BTB from the argument list and this is used for branch prediction
                if btb.find(state.PC) and actual_pc != state.PC_next: # if the branch was in BTB and prediction was wrong then increment the branch misprediction count
                    self.branch_misprediction += 1 

                if not btb.find(state.PC): # if the branch is not in BTB, we need to add it to the BTB
                    # copy various control signals to the state
                    state.MucINC_select = self.MuxINC_select
                    # pc_offset
                    state.PC_offset = self.PC_offset
                    # pc_select
                    state.MuxPC_select = self.MuxPC_select
                    # state_returnaddress
                    state.return_address = self.return_address
                    self.PC_next = state.PC
                    self.IAG(state)
                    
                    if(state.isbranch == 1):
                        btb.enter(True, state.PC, self.PC_next) # whether branch was taken or not, and the current PC and the Target PC
                    else:
                        btb.enter(False, state.PC, self.PC_next)
                    
                    self.reset()
                    self.reset(state)
                    enter = True # set the flag to True as we have entered a new branch into BTB

                else: # if the branch is already in BTB
                    if(state.isbranch == 1):
                        btb.enter(True, state.PC, self.PC_next) # update the BTB entry with the correct branch taken or not
                    else:
                        btb.enter(False, state.PC, self.PC_next)
                if actual_pc != state.PC_next:
                    return True, actual_pc, enter, 1 # first value : whether there was a miprediction, Second value: Actual PCif misprediction occured, Third value: Whether new BTB entry was created, Fourth value: 1 if misprediction occured, 0 otherwise
                else:
                    return False, 0, enter, 3


    # Execute
    def execute(self,state):
        if (state.stall):
            return
        InA=state.RA
        if state.MuxB_select:
            InB=state.Imm
        else:
            InB=state.RB
            
        state.MDR = nhex(state.registerData)
        state.MDR = '0x' + ('0' * (10-len(state.MDR))) + state.MDR[2:]

        for i in range(15):
            if(state.ALU_OP[i]==1):
                if i==0:
                    state.registerData=InA+InB
                    break
                elif i==1:
                    state.registerData=InA-InB
                    break
                elif i==2:
                    if(InB!=0):
                        state.registerData=InA/InB
                    break
                elif i==3:
                    state.registerData=InA*InB
                    break
                elif i==4:
                    if(InB!=0):
                        state.registerData=InA-InB
                    break
                elif i==5:
                    state.registerData=InA^InB
                    break
                elif i==6:
                    if (InB>=0):
                        state.registerData=InA<<InB
                    break
                elif i==7:
                    # SRA (Shift Right Arithmetic) implementation
                    if (InB>=0):
                        # Preserve sign bit when shifting right
                        sign_bit = InA & 0x80000000
                        result = InA >> InB
                        # If original number was negative, fill with 1s
                        if sign_bit:
                            mask = (1 << 32) - 1
                            for j in range(InB):
                                mask = mask ^ (1 << (31 - j))
                            result = result | mask
                        state.registerData = result
                    break
                elif i==8:
                    if (InB>=0):
                        state.registerData=InA>>InB
                    break
                elif i==9:
                    state.registerData=InA|InB
                    break
                elif i==10:
                    state.registerData=InA&InB
                    break
                # Branch Operations
                elif i==11:  # BLT
                    if(InA<InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==12:  # BEQ
                    if(InA==InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==13:  # BNE
                    if(InA!=InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==14:  # BGE
                    if(InA>=InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                else:
                    break

    # Memory Access
    def memoryAccess(self,state):
        if not self.pipeliningEnabled:  # if piplining is disabeled, we call IAG to calculate next PC 
            self.IAG(state)

        if state.stall: # if piplinine is stalled , return immediately without doing anything (USED FOR HANDLING HAZARDS)
            return
        
        # How to update RY?
        if state.MuxY_select == 0: # if the MuxY_select is 0, then the RY is the register data
            state.RY = state.registerData
        elif state.MuxY_select == 1: # if the MuxY_select is 1, then the RY is the memory data
            # Whether to access dataMemory?
            if state.MuxMA_select == False: # if muxMA_select is false , set MAR to the computed address and this address comes form ALU calculations
                state.MAR = state.registerData

                # Memory Read (Load Instructions)
                if state.mem_read:
                    if state.numBytes == 1:
                        tmp = self.dataMemory[state.MAR]
                        state.RY = nint(tmp,16,8) # convert to integer with 8 bit sign extension
                    elif state.numBytes == 2:
                        tmp = self.dataMemory[state.MAR + 1] + self.dataMemory[state.MAR] # read two bytes from memory and concatenate them, in little endian format
                        state.RY = nint(tmp,16,16) 
                    elif state.numBytes == 4:
                        tmp = self.dataMemory[state.MAR + 3] + self.dataMemory[state.MAR + 2] + self.dataMemory[state.MAR + 1] + self.dataMemory[state.MAR]
                        state.RY = nint(tmp,16,32)
                    state.registerData = state.RY
                    
                # Memory Write (Store Instructions)
                elif state.mem_write:
                    if state.numBytes == 1:
                        self.dataMemory[state.MAR] = state.MDR[8:10]
                    if state.numBytes == 2:
                        self.dataMemory[state.MAR] = state.MDR[8:10]
                        self.dataMemory[state.MAR + 1] = state.MDR[6:8]
                    if state.numBytes == 4:
                        self.dataMemory[state.MAR] = state.MDR[8:10]
                        self.dataMemory[state.MAR + 1] = state.MDR[6:8]
                        self.dataMemory[state.MAR + 2] = state.MDR[4:6]
                        self.dataMemory[state.MAR + 3] = state.MDR[2:4]
        elif state.MuxY_select == 2: # if the MuxY_select is 2, then the RY is the PC + 4
            state.RY = state.PC + 4
        
    # Write Back 
    def writeBack(self, state):
        if not state.stall: # if the pipeline is not stalled, then we can write back the result to the register
            if state.registerWrite and state.RD != 0: # if the register write is enabled and the destination register is not 0
                tmp = nhex(state.RY) # convert the result to hexadecimal format
                tmp = '0x' + ('0' * (10 - len(tmp))) + tmp[2:] # add leading zeros to make it 10 characters long
                self.registers[state.RD] = tmp # write the result to the destination register

    def update_stack_state(self):
        """
        Records the current state of the call stack after each cycle.
        This method is called at the end of each cycle to capture the stack state.
        """
        print(f"\nUpdating stack state at cycle {self.Total_instructions}")
        print(f"Current call stack: {self.call_stack}")
        current_stack = {
            'cycle': self.Total_instructions,
            'stack': [{'return_address': addr['return_address'], 
                      'instruction_type': addr['instruction_type'],
                      'pc': addr['pc']} for addr in self.call_stack]
        }
        print(f"New stack state: {current_stack}")
        self.stack_states.append(current_stack)

        # Print the current stack contents
        print("\nCurrent Stack Contents:")
        if not self.call_stack:
            print("Stack is empty")
        else:
            for i, item in enumerate(self.call_stack):
                print(f"Stack Level {i}:")
                print(f"  Instruction Type: {item['instruction_type']}")
                print(f"  Return Address: 0x{item['return_address']:08x}")
                print(f"  PC: 0x{item['pc']:08x}")

        # Write to stack_states.txt
        try:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'stack_states.txt')

            with open(file_path, 'a') as f:  # Using 'a' for append mode
                f.write(f"\n=== Cycle {self.Total_instructions} ===\n")
                if not self.call_stack:
                    f.write("Stack is empty\n")
                else:
                    for i, item in enumerate(self.call_stack):
                        f.write(f"Stack Level {i}:\n")
                        f.write(f"  Instruction Type: {item['instruction_type']}\n")
                        f.write(f"  Return Address: 0x{item['return_address']:08x}\n")
                        f.write(f"  PC: 0x{item['pc']:08x}\n")
                f.write("-" * 50 + "\n")
            
        except Exception as e:
            print(f"Error writing to stack_states.txt: {str(e)}")

    def push_stack(self, return_address, instruction_type, pc):
        """
        Pushes a return address onto the call stack when a branch or jump instruction is encountered.
        
        Args:
            return_address: The address to return to after the branch/jump
            instruction_type: The type of instruction (JAL, JALR, BEQ, etc.)
            pc: The program counter value of the branch/jump instruction
        """
        print(f"\nPushing to stack:")
        print(f"Return Address: 0x{return_address:08x}")
        print(f"Instruction Type: {instruction_type}")
        print(f"PC: 0x{pc:08x}")
        self.call_stack.append({
            'return_address': return_address,
            'instruction_type': instruction_type,
            'pc': pc
        })
        print(f"Current stack size: {len(self.call_stack)}")

    def pop_stack(self):
        """
        Pops a return address from the call stack when returning from a branch or jump.
        
        Returns:
            The return address entry that was popped, or None if the stack is empty
        """
        if self.call_stack:
            popped_entry = self.call_stack.pop()
            print(f"\nPopping from stack:")
            print(f"Return Address: 0x{popped_entry['return_address']:08x}")
            print(f"Instruction Type: {popped_entry['instruction_type']}")
            print(f"PC: 0x{popped_entry['pc']:08x}")
            return popped_entry
        return None

    def write_stack_states(self):
        import os
        print("\n=== Writing Stack States ===")
        print(f"Number of stack states to write: {len(self.stack_states)}")
        
        try:
            # Get the absolute path to the src directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'stack_states.txt')
            
            print(f"\nFile Information:")
            print(f"Current directory: {current_dir}")
            print(f"Target file path: {file_path}")
            print(f"Directory exists: {os.path.exists(current_dir)}")
            print(f"File exists: {os.path.exists(file_path)}")
            
            print("\nStack States Content:")
            with open(file_path, 'w') as f:
                f.write("=== Current Stack States ===\n\n")
                
                # Write current stack contents
                f.write("Current Stack Contents:\n")
                if not self.call_stack:
                    print("Stack is empty")
                    f.write("Stack is empty\n")
                else:
                    for i, item in enumerate(self.call_stack):
                        stack_entry = f"Stack Level {i}:\n"
                        stack_entry += f"  Instruction Type: {item['instruction_type']}\n"
                        stack_entry += f"  Return Address: 0x{item['return_address']:08x}\n"
                        stack_entry += f"  PC: 0x{item['pc']:08x}\n"
                        print(stack_entry)
                        f.write(stack_entry)
                
                f.write("\n" + "="*50 + "\n\n")
                
                # Write stack states history
                f.write("Stack States History:\n\n")
                for state in self.stack_states:
                    f.write(f"Cycle {state['cycle']}:\n")
                    if not state['stack']:
                        f.write("  Stack is empty\n")
                    else:
                        for item in state['stack']:
                            f.write(f"  Instruction Type: {item['instruction_type']}\n")
                            f.write(f"  Return Address: 0x{item['return_address']:08x}\n")
                            f.write(f"  PC: 0x{item['pc']:08x}\n")
                            f.write("\n")
                    f.write("-" * 50 + "\n")
            
            print("\nSuccessfully wrote to file!")
            
        except Exception as e:
            print(f"\nError Details:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Directory contents: {os.listdir('.')}")
            print(f"Parent directory contents: {os.listdir('..')}")