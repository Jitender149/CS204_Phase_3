Pipelined Execution Workflow (With Forwarding - Frontend/Backend Interaction)

This describes the 5-stage pipeline flow using DATA FORWARDING to minimize stalls, emphasizing frontend/backend roles.

1.  **Setup:**
    *   **Frontend:** User loads code and selects "Pipelined" mode, ensuring "Forwarding" is ENABLED.
    *   **Frontend:** Sends `/api/load_code` request with mode selection.
    *   **Backend:** Loads code, initializes PC, registers, stats. Initializes pipeline registers to NOP/stalled state. Sets mode to pipelined, forwarding enabled.
    *   **Backend:** Responds with success/initial state.
    *   **Frontend:** Displays initial state.

2.  **Step Execution (One Clock Cycle):**
    *   **Frontend:** User clicks "Step".
    *   **Frontend:** Sends `/api/step` request.
    *   **Backend:** Receives request. Executes `Processor.run_one_cycle()`.
    *   **Backend:** Simulates **one clock cycle**:
        *   **HDU Check (Start of Cycle):** HDU examines instructions in ID, EX, MEM, WB.
        *   **Hazard Determination & Forwarding:**
            *   If a RAW hazard is detected (e.g., `ADD x1` in EX, `SUB reads x1` in ID), the HDU **checks if forwarding is possible**: 
                *   Can EX result (available end-of-cycle via EX/MEM latch) be fed to EX input next cycle? YES.
                *   HDU generates control signals for EX stage input MUXes to select data from EX/MEM latch instead of Register File.
                *   **Result:** NO STALL needed for this hazard.
            *   If a RAW hazard is detected (e.g., `ADD x1` in MEM, `SUB reads x1` in ID):
                *   Can MEM result (available end-of-cycle via MEM/WB latch) be fed to EX input next cycle? YES.
                *   HDU generates control signals for EX stage input MUXes to select data from MEM/WB latch.
                *   **Result:** NO STALL needed.
            *   If a **Load-Use Hazard** is detected (e.g., `LW x1` in EX, `ADD reads x1` in ID):
                *   The LW data is only available from MEM stage *at the end* of the *next* cycle. The ADD needs it in EX *at the start* of the *next* cycle.
                *   Forwarding is NOT possible in time.
                *   HDU generates **STALL** signals (Stall IF/ID, Stall PC, Force NOP into ID/EX), similar to the no-forwarding case.
                *   **Result:** 1 Cycle Stall.
        *   **Stage Execution (Concurrent):**
            *   WB: Instruction from MEM/WB writes back.
            *   MEM: Instruction from EX/MEM accesses memory / passes data.
            *   EX: Instruction from ID/EX performs ALU op (using potentially forwarded data, or receiving NOP if stalled).
            *   ID: Instruction from IF/ID decodes (or holds if stalled).
            *   IF: Fetches instruction at PC (or holds if stalled).
        *   **PC Update:** PC updates to PC+4 unless stalled or branch/jump taken.
        *   **Pipeline Register Update:** Latches update based on stall signals.
    *   **Backend:** Updates internal state (registers, memory, PC, pipeline latches, stats - including cycles, stalls, specific hazard counts).
    *   **Backend:** Gathers state for response:
        *   `pc`: Current PC.
        *   `registers`: Current register state.
        *   `pipeline_stages`: Same structure as no-forwarding case, showing instruction/state/stall/bubble status per stage.
        *   `hazard_info`: {
                'stalling_IF': bool, 'stalling_ID': bool, 'insert_bubble_EX': bool,
                'detected_hazards': [ description... ],
                **'forwarding_paths'**: { 
                    'EX_rs1_src': 'MEM/WB' | 'EX/MEM' | 'RegFile', 
                    'EX_rs2_src': 'MEM/WB' | 'EX/MEM' | 'RegFile' 
                } 
            } (Crucially includes which paths were used for forwarding this cycle).
        *   `stats`: Updated stats.
    *   **Backend:** Sends JSON response.
    *   **Frontend:** Receives response.
    *   **Frontend:** Updates React state:
        *   Updates the Pipeline Diagram (`Simulator.js`): Populates stage boxes. Uses `hazard_info.stalling_*` to show stalls/glow. Uses **`hazard_info.forwarding_paths`** to draw visual indicators (lines/arrows) showing data being forwarded (e.g., an arrow from the output of the MEM stage box connecting to the input of the EX stage box if `EX_rs*_src` is `MEM/WB`).
        *   Updates Register/Memory/Stats views.

3.  **Loop:**
    *   Repeats for each "Step", simulating one clock cycle, prioritizing forwarding but stalling when necessary (Load-Use, Control). 