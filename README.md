# RISC-V Simulator
## Phase 3 (Pipelined Implementation)

### Overview
This is a RISC-V simulator that supports pipelined execution of instructions with a modern web-based visualization interface. The simulator features a comprehensive pipeline implementation with data forwarding, branch prediction, and detailed visualization of various components including registers, memory, data hazards, and the call stack.

### Features
- **Pipelined Execution**: Support for 5-stage pipeline (IF, ID, EX, MEM, WB)
- **Data Forwarding**: Optional data forwarding to reduce stalls
- **Branch Prediction**: Branch Target Buffer (BTB) implementation
- **Visualization Components**:
  - Register File Visualization
  - Memory Content Display
  - Data Hazard Analysis
  - Pipeline Simulation
  - Call Stack Visualization
- **Interactive Controls**: Cycle-by-cycle execution with detailed statistics
- **Modern UI**: Responsive design with intuitive navigation

### Directory Structure
```
phase-3
    |- frontend
        |- public
        |- src
            |- Components
                |- Stack.js
                |- Stack.css
                |- MemoryScreen.js
                |- RegisterScreen.js
                |- DataHazardScreen.js
                |- Simulator.js
                |- input.js
            |- App.js
            |- App.css
    |- src
        |- main.py
        |- processor.py
        |- state.py
        |- hdu.py
        |- btb.py
        |- utility.py
        |- demofile.txt
        |- reg.txt
        |- data.txt
        |- stats.txt
        |- cycle.txt
        |- branch_prediction.txt
        |- stack_states.json
        |- test
            |- fibo.mc
            |- bubble.mc
            |- factorial.mc
        |- app.py
        |- jsonify.py
    |- README.md
```

### How to Run
1. Start the backend server:
   ```bash
   cd src
   python app.py
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

4. Upload your RISC-V machine code file (.mc) and configure the simulation options:
   - Enable/disable pipelining
   - Enable/disable data forwarding
   - Configure register and pipeline register display options

5. Click "Submit" to start the simulation

### Visualization Components

#### 1. Register File
- Displays all 32 RISC-V registers
- Shows current values in hexadecimal format
- Updates in real-time during simulation

#### 2. Memory Content
- Visualizes data memory contents
- Displays addresses and values in hexadecimal
- Supports scrolling through memory locations

#### 3. Data Hazards
- Shows RAW, WAR, and WAW hazards
- Displays forwarding paths when enabled
- Highlights affected pipeline stages

#### 4. Pipeline Simulation
- Interactive 5-stage pipeline visualization
- Shows instruction flow through stages
- Highlights stalls and forwarding
- Displays current instruction in each stage

#### 5. Call Stack
- Visualizes the call stack during execution
- Shows stack frames with:
  - Return addresses
  - Instruction types
  - Program counter values
- Supports cycle-by-cycle navigation
- Modern UI with hover effects and animations

### Output Files
- `reg.txt`: Final register values
- `data.txt`: Final memory contents
- `stats.txt`: Performance statistics
- `cycle.txt`: Detailed cycle information
- `branch_prediction.txt`: Branch prediction statistics
- `stack_states.json`: Call stack history

### Performance Statistics
The simulator tracks and displays:
- Total clock cycles
- Instructions executed
- CPI (Cycles per Instruction)
- Data transfer instructions
- ALU instructions
- Control instructions
- Number of stalls
- Branch mispredictions
- Data and control hazards

### Documentation
For detailed implementation information, please refer to `design-doc.docx`.

### Technologies Used
- **Backend**: Python
- **Frontend**: React.js
- **Styling**: CSS3, Tailwind CSS
- **Visualization**: Custom React components

### Contributing
Feel free to submit issues and enhancement requests!