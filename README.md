# RISC-V Simulator
## Phase 2 (Pipelined Implementation)
### Overview
This is a RISC-V simulator which supports piplined execution of instructions. There are various input knobs that can be set by the user to enable/disable pipelining, data forwarding, printing register file and printing pipeline registers for all or a specific instruction.

### Directory Structure
```
phase-2
    |- frontend
        |- public
        |- src
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
        |- test
            |- fibo.mc
            |- bubble.mc
            |- factorial.mc
        |- app.py
        |- jsonify.py
    |- README.md
        

```

### How to run
1. Run the following command in the src directory.

        python app.py
2. Then, run the following commands on terminal in the frontend directory.

        npm i
        npm start
3. A GUI window opens where you have to upload the .mc that contains the machine code you want to run and check/uncheck some knobs, then hit submit.
4. The program runs and GUI redirects and displays various information corresponding to the input program i.e. final register values, data memory values, data hazards and control hazards and a simulation for understanding each step of execution.

### Documentation
Read the `design-doc.docx` for more information about the implementation.