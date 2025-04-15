# Instructions/State Class
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

        self.stall = False
        self.branch_taken=False
        self.isbranch=0
        # Control Signals
        self.registerWrite=False
        self.MuxB_select=False
        self.MuxY_select=False
        self.mem_write=False
        self.mem_read=False
        self.MuxMA_select=False
        self.MuxPC_select=False
        self.MuxINC_select=False
        self.numBytes=0
        # Forwarding Signals
        self.decode_forwarding_op1 = False
        self.decode_forwarding_op2 = False

    
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
