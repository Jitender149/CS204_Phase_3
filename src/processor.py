from collections import defaultdict
from btb import *
from utility import *
class processor:
    def __init__(self, file1):
        self.dataMemory = defaultdict(lambda: '00') # initialising data memory
        self.instructionMemory = defaultdict(lambda: '00') # initialising instruction memory
        self.registers = ['0x00000000' for i in range(32)] # initialising registers
        self.registers[2]='0x7FFFFFF0' # sp
        self.registers[3]='0x10000000' # gp
        self.loadProgramMemory(file1) # read program.mc file to load our data and intruction memory
        self.pipeliningEnabled = False # knob for pipelining
        self.PC_next = 0 # Next PC address
        self.PC_offset = 0 # PC offset
        self.return_address = -1 # return address
        self.terminate = False # flag to terminate the program
        # Control Signals
        self.registerWrite=False
        self.MuxB_select=False
        self.MuxY_select=0
        self.mem_write=False
        self.mem_read=False
        self.MuxMA_select=False
        self.MuxPC_select=False
        self.MuxINC_select=False
        self.numBytes=0
        # Counts
        self.Total_instructions=0 # Total number of instructions executed
        self.ALU_instructions=0 # Total number of ALU instructions executed
        self.memory_instructions=0  # Total number of memory instructions executed
        self.control_instructions=0 # Total number of control instructions executed
        self.branch_misprediction=0 # Total number of branch mispredictions
        
        self.allStall=False
        self.riscvCode = defaultdict(lambda: -1)

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
    
    # Function to populate the instruction & data memory using the program.mc file    
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
                    if(flag):
                        idx = int(address[2:], 16)
                        self.instructionMemory[idx] = instruction[8:10]
                        self.instructionMemory[idx+1] = instruction[6:8]
                        self.instructionMemory[idx+2] = instruction[4:6]
                        self.instructionMemory[idx+3] = instruction[2:4]
                    else:
                        idx = int(address[2:], 16)
                        instruction = '0x' + (10 - len(instruction))*'0' + instruction[2:]
                        self.dataMemory[idx] = instruction[8:10]
                        self.dataMemory[idx+1] = instruction[6:8]
                        self.dataMemory[idx+2] = instruction[4:6]
                        self.dataMemory[idx+3] = instruction[2:4]
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
    def fetch(self, state, *args):
        if state.stall == True:
            return
        state.IR = '0x' + self.instructionMemory[state.PC + 3] + self.instructionMemory[state.PC + 2] + self.instructionMemory[state.PC + 1] + self.instructionMemory[state.PC]
        
        if self.allStall:
            state.stall=True
            return

        if not self.pipeliningEnabled:
            return
        
        btb=args[0]
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
            return False, 0, False, 0
        
        if state.IR == '0x00000000':
            self.terminate = True
            state.stall = True
            self.allStall = True
            return False, 0, False, 0
        
        self.Total_instructions += 1

        for i in range(15):
            state.ALU_OP[i] = False

        instruction = bin(int(state.IR[2:], 16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction

        # Opcode and func3
        opcode = instruction[25:32]
        func3 = int(instruction[17:20], 2)

        # R Format
        if(opcode == '0110011'):
            state.generateControlSignals(True, False, 0, False, False, False, True, False, 4)
            state.RD = int(instruction[20:25], 2)
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

            state.RA = nint(self.registers[state.RS1][2:], 16)
            state.RB = nint(self.registers[state.RS2][2:], 16)
            self.ALU_instructions += 1
            
        # I Format
        elif(opcode == '0010011' or opcode == '0000011' or opcode == '1100111'):
            state.RD = int(instruction[20:25],2)
            state.RS1 = int(instruction[12:17],2)
            state.Imm = int(instruction[0:12],2)
            
            if(state.Imm > 2047):
                state.Imm -= 4096
                
            # LB/LH/LW
            if(opcode == '0000011'):
                state.ALU_OP[0] = True
                # LB Instruction
                if(func3 == 0x0):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,1)
                    code = 'LB x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                # LH Instruction
                elif(func3 == 0x1):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,2)
                    code = 'LH x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                # LW Instruction
                elif(func3 == 0x2):
                    state.generateControlSignals(True,True,1,True,False,False,True,False,4)
                    code = 'LW x' + str(state.RD) + ', ' + str(state.Imm) + '(x' + str(state.RS1) + ')'
                else:
                    print("Unknown instruction")
                    exit(1)
            
                state.RA = int(self.registers[state.RS1][2:], 16)
                self.memory_instructions += 1
            
            # ADDI/ANDI/ORI/XORI/SLLI/SRLI
            elif(opcode == '0010011'):
                state.generateControlSignals(True,True,0,False,False,False,True,False,4)
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
                state.RA = nint(self.registers[state.RS1][2:], 16)
                self.ALU_instructions += 1
            
            # JALR
            elif(opcode == '1100111'):
                state.generateControlSignals(True,False,2,False,False,False,False,True,4)
                # JALR Instruction
                if(func3 == 0x0):
                    state.ALU_OP[0] = True
                    code = 'JALR x' + str(state.RD) + ', x' + str(state.RS1) + ', ' + str(state.Imm)
                else:
                    print("Unknown Error")
                    exit(1)
                state.isbranch=1
                state.RA = nint(self.registers[state.RS1][2:], 16)
                state.return_address = state.RA
                self.return_address = state.RA
                self.MuxPC_select = True
                self.control_instructions += 1
                state.registerData = state.PC + 4
        
        # S Format
        elif(opcode == '0100011'):
            state.RS1 = int(instruction[12:17],2)
            state.RS2 = int(instruction[7:12],2)
            state.Imm = int(instruction[0:7] + instruction[20:25],2)
            state.Imm = ImmediateSign(state.Imm,12)
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
            
            state.RA = int(self.registers[state.RS1][2:], 16)
            state.RB = int(self.registers[state.RS2][2:], 16)
            state.registerData = state.RB
            self.memory_instructions += 1
        
        # B Format
        elif(opcode == '1100011'):
            state.RS1 = int(instruction[12:17], 2)
            state.RS2 = int(instruction[7:12], 2)
            
            state.RA = nint(self.registers[state.RS1][2:], 16)
            state.RB = nint(self.registers[state.RS2][2:], 16)
            
            state.Imm = int(instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24],2)
            state.Imm = ImmediateSign(state.Imm,12)
            state.Imm *= 2
            # BEQ Instruction
            if(func3 == 0x0):
                state.ALU_OP[12] = True
                code = 'BEQ x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
            # BNE Instruction
            elif(func3 == 0x1):
                state.ALU_OP[13] = True
                code = 'BNE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
            # BLT Instruction
            elif(func3 == 0x4):
                state.ALU_OP[11] = True
                code = 'BLT x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
            # BGE Instruction
            elif(func3 == 0x5):
                state.ALU_OP[14] = True
                code = 'BGE x' + str(state.RS1) + ', x' + str(state.RS2) + ', ' + str(state.Imm)
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
            # JAL Instruction
            state.RD = int(instruction[20:25],2)
            state.Imm = int(instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11],2)
            state.Imm =  ImmediateSign(state.Imm,20)
            state.Imm *= 2
            state.ALU_OP[12] = True
            code = 'JAL x' + str(state.RD) + ', ' + str(state.Imm)
            state.RA = 0
            state.RB = 0
            state.isbranch=1
            state.generateControlSignals(True,False,2,False,False,False,True,True,0)
            self.control_instructions += 1
            state.registerData = state.PC + 4
        
        else:
            print("Unknown Instruction")
            exit(1)
        
        self.riscvCode[state.PC] = code

        if self.pipeliningEnabled:
            enter = False
            if state.isbranch == 0:
                return False, 0, False, 0
            else:
                self.execute(state)
                self.PC_next = state.PC
                self.IAG(state)
                actual_pc = self.PC_next

                btb = args[0]
                if btb.find(state.PC) and actual_pc != state.PC_next:
                    self.branch_misprediction += 1

                if not btb.find(state.PC):
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
                        btb.enter(True, state.PC, self.PC_next)
                    else:
                        btb.enter(False, state.PC, self.PC_next)
                    
                    self.reset()
                    self.reset(state)
                    enter = True

                else:
                    if(state.isbranch == 1):
                        btb.enter(True, state.PC, self.PC_next)
                    else:
                        btb.enter(False, state.PC, self.PC_next)
                if actual_pc != state.PC_next:
                    return True, actual_pc, enter, 1
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
                    #please write sra code here.
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
                elif i==11:
                    if(InA<InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==12:
                    if(InA==InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==13:
                    if(InA!=InB):
                        state.MuxINC_select=True
                        state.PC_offset = state.Imm
                    self.PC_offset = state.Imm
                    self.MuxINC_select = True
                    break
                elif i==14:
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
        if not self.pipeliningEnabled:
            self.IAG(state)

        if state.stall:
            return
        
        # How to update RY?
        if state.MuxY_select == 0:
            state.RY = state.registerData
        elif state.MuxY_select == 1:
            # Whether to access dataMemory?
            if state.MuxMA_select == False:
                state.MAR = state.registerData

                # Memory Read (Load Instructions)
                if state.mem_read:
                    if state.numBytes == 1:
                        tmp = self.dataMemory[state.MAR]
                        state.RY = nint(tmp,16,8)
                    elif state.numBytes == 2:
                        tmp = self.dataMemory[state.MAR + 1] + self.dataMemory[state.MAR]
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
        elif state.MuxY_select == 2:
            state.RY = state.PC + 4
        
    # Write Back 
    def writeBack(self, state):
        if not state.stall:
            if state.registerWrite and state.RD != 0:
                tmp = nhex(state.RY)
                tmp = '0x' + ('0' * (10 - len(tmp))) + tmp[2:]
                self.registers[state.RD] = tmp

				
        
        

