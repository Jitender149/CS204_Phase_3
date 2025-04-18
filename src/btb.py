# If the instruction is jal/jalr, we are always making the prediction as 'true'.
# Otherwise, we are making the prediction 'true' if we are going back and 'false' if we are going forward.

# class BTB:
#     def __init__(self):
#         self.table={} # initialize an empty dictionary to store the branch prediction table
    
#     def find(self, pc):  # finding the branch prediction table entry for the given PC address
#         if pc in self.table.keys(): # if the PC address is present in the table
#             return True # return true
#         return False # return false
    
#     def enter(self, is_jump, pc, next_address): # adding a new entry to the branch prediction table
#         if is_jump:
#             self.table[pc] = [True,next_address]
#         elif next_address > pc: # if the next address is greater than the current PC address
#             self.table[pc] = [False,next_address] # update the table with false and the next address        
#         else:
#             self.table[pc] = [True,next_address] # update the table with true and the next address

#     def predict(self, pc):
#         return self.table[pc][0]
    
#     def next_add(self, pc):
#         return self.table[pc][1]
    

# 1 bit dynamic predictor
class BTB:
    def __init__(self):
        self.table = {}  # initialize an empty dictionary to store the branch prediction table
    
    def find(self, pc):  # finding the branch prediction table entry for the given PC address
        if pc in self.table.keys():  # if the PC address is present in the table
            return True  # return true
        return False  # return false
    
    def enter(self, is_jump, pc, next_address):  # adding a new entry to the branch prediction table
        if not self.find(pc):
            # For first-time branches, always predict taken
            self.table[pc] = [True, next_address]
        else:
            # If entry exists, update the prediction bit based on actual outcome
            self.table[pc][0] = is_jump
            self.table[pc][1] = next_address
    
    def predict(self, pc):
        if pc in self.table:
            return self.table[pc][0]
        # For first-time branches not yet in table, predict taken
        return True
    
    def next_add(self, pc):
        if pc in self.table:
            return self.table[pc][1]
        # For first-time branches, return PC+4 as a default target
        return pc + 4
    
# for the first time we wait till the branch instruction is executed
# then we update the prediction bit based on the actual outcome
# then we update the next address based on the actual outcome
# then we return the prediction bit and the next address


