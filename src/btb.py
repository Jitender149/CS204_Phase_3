# If the instruction is jal/jalr, we are always making the prediction as 'true'.
# Otherwise, we are making the prediction 'true' if we are going back and 'false' if we are going forward.
class BTB:
    def __init__(self):
        self.table={}
    
    def find(self, pc):
        if pc in self.table.keys():
            return True
        return False
    
    def enter(self, is_jump, pc, next_address):
        if is_jump:
            self.table[pc] = [True,next_address]
        elif next_address > pc:
            self.table[pc] = [False,next_address]
        else:
            self.table[pc] = [True,next_address]

    def predict(self, pc):
        return self.table[pc][0]
    
    def next_add(self, pc):
        return self.table[pc][1]
    


    