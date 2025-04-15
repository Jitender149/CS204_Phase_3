# Instructions/State Class
# This class is used to store the state of the instruction
# It acts as a container for all the information needed to process an instruction through each pipline stage
# state.py defines the State class which represents the state of an instruction as it moves through the pipeline
class State:
    def __init__(self, PC = 0):
        self.PC = PC
        self.PC_next = 0
        self.PC_offset = 0
        self.return_address = -1
        self.IR = '0x00000000'
        self.RS1 = -1
        self.RS2 = -1
        self.RD = -1
        self.RA = 0
        self.RB = 0
        self.RY = 0
        self.RZ = 0
        self.RM = 0
        self.MDR = '00000000'
        self.MAR = 0
        self.Imm = 0
        self.ALU_OP = [0 for i in range(15)]
        self.registerData = 0

        self.stall = False  # by default the instruction is not stalled
        self.branch_taken=False # by default the branch is not taken
        self.isbranch=0 # by default the instruction is not a branch
        # Control Signals
        self.registerWrite=False # by default the register is not written
        self.MuxB_select=False # by default the second ALU input is not selected
        self.MuxY_select=False # by default the write back data source is not selected
        self.mem_write=False # by default the memory is not written
        self.mem_read=False # by default the memory is not read
        self.MuxMA_select=False # by default the memory address source is not selected
        self.MuxPC_select=False # by default the PC source is not selected
        self.MuxINC_select=False # by default the PC increment source is not selected
        self.numBytes=0 # by default the number of bytes is 0
        # Forwarding Signals
        self.decode_forwarding_op1 = False # by default the first operand is not forwarded
        self.decode_forwarding_op2 = False # by default the second operand is not forwarded
        # we have M->M, M->E, E->E, M->D,E->D forwarding
    
    def generateControlSignals(self,RW,MBS,MYS,MR,MW,MMA,MPC,MINC,NUM):
        self.registerWrite = RW
        self.MuxB_select = MBS
        self.MuxY_select = MYS
        self.mem_read = MR
        self.mem_write = MW
        self.MuxMA_select = MMA
        self.MuxPC_select = MPC
        self.MuxINC_select = MINC
        self.numBytes = NUM
