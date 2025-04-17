Pipelined Execution Workflow (No Forwarding - Frontend/Backend Interaction)

This describes the 5-stage pipeline flow with hazard detection via STALLING only, emphasizing frontend/backend roles.

1.  **Setup:**
    *   **Frontend:** User loads code and selects "Pipelined" mode, ensuring "Forwarding" is disabled.
    *   **Frontend:** Sends `/api/load_code` request with mode selection.
    *   **Backend:** Loads code, initializes PC, registers, stats. Initializes pipeline registers (IF/ID, ID/EX, EX/MEM, MEM/WB) usually to a NOP/stalled state. Sets mode to pipelined, forwarding disabled.
    *   **Backend:** Responds with success/initial state.
    *   **Frontend:** Displays initial state (often empty/stalled pipeline).

2.  **Step Execution (One Clock Cycle):**
    *   **Frontend:** User clicks "Step".
    *   **Frontend:** Sends `/api/step` request.
    *   **Backend:** Receives request. Executes `Processor.run_one_cycle()` (or similar) for pipelined mode.
    *   **Backend:** Simulates the activity within **one clock cycle** across all 5 stages concurrently:
        *   **HDU Check (Start of Cycle):** The Hazard Detection Unit examines instructions in ID, EX, MEM, WB stages to detect RAW data hazards and potential control hazards.
        *   **Stall Determination:** If a RAW hazard is detected AND forwarding is disabled, the HDU determines stall signals.
            *   Example: `ADD x1` in EX, `SUB reads x1` in ID -> STALL.
            *   HDU generates signals: Stall IF/ID latch, Stall PC update, Force NOP into ID/EX latch.
        *   **Stage Execution (Concurrent):**
            *   WB: Instruction from MEM/WB writes back (if required).
            *   MEM: Instruction from EX/MEM accesses memory or passes data.
            *   EX: Instruction from ID/EX performs ALU operation (or receives a NOP if stalled).
            *   ID: Instruction from IF/ID decodes (or holds if stalled).
            *   IF: Fetches instruction at PC (or holds if stalled).
        *   **PC Update:** PC is updated to PC+4 *unless* stalled or a branch/jump occurred.
        *   **Pipeline Register Update (End of Cycle):** Based on stall signals, pipeline registers latch new values or retain old ones/load NOPs.
    *   **Backend:** Updates internal state (registers, memory, PC, pipeline latches, stats - incrementing cycle count, stall count if applicable).
    *   **Backend:** Gathers state for response:
        *   `pc`: Current PC (may or may not have incremented).
        *   `registers`: Current state of register file.
        *   `pipeline_stages`: {
                'IF': { 'instruction': hex_or_asm, 'pc': value },
                'ID': { 'instruction': hex_or_asm, 'pc': value, 'is_stalled': bool },
                'EX': { 'instruction': hex_or_asm, 'pc': value, 'is_bubble': bool },
                'MEM': { 'instruction': hex_or_asm, 'pc': value, 'is_bubble': bool },
                'WB': { 'instruction': hex_or_asm, 'pc': value, 'is_bubble': bool }
            } (Content represents state *after* the cycle completed).
        *   `hazard_info`: {
                'stalling_IF': bool,
                'stalling_ID': bool,
                'insert_bubble_EX': bool,
                'detected_hazards': [ description... ]
            } (Indicating active stalls for this cycle).
        *   `stats`: Updated stats.
    *   **Backend:** Sends JSON response.
    *   **Frontend:** Receives response.
    *   **Frontend:** Updates React state:
        *   Updates the Pipeline Diagram (`Simulator.js`): Populates each stage box with `pipeline_stages` data. Uses `hazard_info` to visually indicate stalls (e.g., graying out, adding "STALL" text, showing NOP/bubble in EX). If `is_stalled` is true for ID, it applies the red glow via the `.glow` class logic.
        *   Updates Register/Memory/Stats views.

3.  **Loop:**
    *   Repeats for each "Step", simulating one clock cycle advancement (or stall) of the pipeline. 