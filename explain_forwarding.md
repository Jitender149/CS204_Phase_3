# RISC-V Pipeline Forwarding Cases

This document explains the different forwarding cases in the RISC-V pipeline with examples and diagrams.

## 1. Writeback to Execute (M -> E) Forwarding

### Case 1: Forwarding to RS1
```assembly
LW x1, 0(x2)    # WB stage: Load value into x1
ADD x3, x1, x4  # EX stage: Use x1 as first operand
```
```
Pipeline:
WB: LW x1, 0(x2)  → x1 = [loaded value]
MEM: -             → -
EX: ADD x3, x1, x4 → RA = [forwarded value]
ID: -             → -
IF: -             → -
```

### Case 2: Forwarding to RS2
```assembly
LW x1, 0(x2)    # WB stage: Load value into x1
ADD x3, x4, x1  # EX stage: Use x1 as second operand
```
```
Pipeline:
WB: LW x1, 0(x2)  → x1 = [loaded value]
MEM: -             → -
EX: ADD x3, x4, x1 → RB = [forwarded value]
ID: -             → -
IF: -             → -
```

## 2. Memory to Execute (M -> E) Forwarding

### Case 1: Forwarding to RS1
```assembly
ADD x1, x2, x3  # MEM stage: Result in x1
ADD x4, x1, x5  # EX stage: Use x1 as first operand
```
```
Pipeline:
WB: -             → -
MEM: ADD x1, x2, x3 → x1 = [result]
EX: ADD x4, x1, x5 → RA = [forwarded value]
ID: -             → -
IF: -             → -
```

### Case 2: Forwarding to RS2
```assembly
ADD x1, x2, x3  # MEM stage: Result in x1
ADD x4, x5, x1  # EX stage: Use x1 as second operand
```
```
Pipeline:
WB: -             → -
MEM: ADD x1, x2, x3 → x1 = [result]
EX: ADD x4, x5, x1 → RB = [forwarded value]
ID: -             → -
IF: -             → -
```

## 3. Execute to Execute (E -> E) Forwarding

### Case 1: Load Instruction
```assembly
LW x1, 0(x2)    # MEM stage: Load value into x1
SW x3, 0(x1)    # EX stage: Use x1 as address
```
```
Pipeline:
WB: -             → -
MEM: LW x1, 0(x2)  → x1 = [loaded value]
EX: SW x3, 0(x1)   → registerData = [forwarded value]
ID: -             → -
IF: -             → -
```

### Case 2: Non-Load Instruction
```assembly
ADD x1, x2, x3  # MEM stage: Result in x1
ADD x4, x1, x5  # EX stage: Use x1 as operand
```
```
Pipeline:
WB: -             → -
MEM: ADD x1, x2, x3 → x1 = [result]
EX: ADD x4, x1, x5 → RA = [forwarded value]
ID: -             → -
IF: -             → -
```

## 4. Memory to Decode (M -> D) Forwarding

### Case 1: Branch Instruction
```assembly
ADD x1, x2, x3  # WB stage: Result in x1
BEQ x1, x4, label  # ID stage: Use x1 for comparison
```
```
Pipeline:
WB: ADD x1, x2, x3  → x1 = [result]
MEM: -              → -
EX: -              → -
ID: BEQ x1, x4, label → RA = [forwarded value]
IF: -              → -
```

### Case 2: JALR Instruction
```assembly
ADD x1, x2, x3  # WB stage: Result in x1
JALR x1, 0(x5)  # ID stage: Use x1 as target
```
```
Pipeline:
WB: ADD x1, x2, x3  → x1 = [result]
MEM: -              → -
EX: -              → -
ID: JALR x1, 0(x5)  → RA = [forwarded value]
IF: -              → -
```

## 5. Execute to Decode (E -> D) Forwarding

### Case 1: Control Instruction Dependency
```assembly
ADD x1, x2, x3  # EX stage: Result in x1
BEQ x1, x4, label  # ID stage: Use x1 for comparison
```
```
Pipeline:
WB: -             → -
MEM: -            → -
EX: ADD x1, x2, x3 → x1 = [result]
ID: BEQ x1, x4, label → RA = [forwarded value]
IF: -             → -
```

## Forwarding Path Diagrams

### M -> E Forwarding
```
WB: [Value] → MEM: [Forward] → EX: [Use]
```

### E -> E Forwarding
```
MEM: [Value] → EX: [Forward] → EX: [Use]
```

### M -> D Forwarding
```
WB: [Value] → MEM: [Forward] → ID: [Use]
```

### E -> D Forwarding
```
MEM: [Value] → EX: [Forward] → ID: [Use]
```

## Key Points

1. **Load Instructions**:
   - Require special handling
   - May cause stalls if data isn't ready
   - Forwarding paths depend on instruction type

2. **Store Instructions**:
   - Use forwarded values as addresses
   - Different handling than other instructions
   - Forward to registerData instead of RA/RB

3. **Control Instructions**:
   - Need immediate forwarding
   - Critical for correct branch prediction
   - May require stalls if data isn't ready

4. **Forwarding Priorities**:
   - WB → EX has highest priority
   - MEM → EX is next
   - E → E and M → D are last resort 