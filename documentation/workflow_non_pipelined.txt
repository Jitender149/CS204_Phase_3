Non-Pipelined Execution Workflow (Frontend/Backend Interaction)

This describes the flow when the simulator runs in non-pipelined mode, emphasizing frontend/backend roles.

1.  **Setup:**
    *   **Frontend:** User loads code and selects "Non-Pipelined" mode.
    *   **Frontend:** Sends `/api/load_code` request with mode selection.
    *   **Backend:** Loads code into memory, initializes PC and registers. Sets internal mode to non-pipelined.
    *   **Backend:** Responds with success/initial state.
    *   **Frontend:** Displays initial state (PC, registers, memory).

2.  **Step Execution:**
    *   **Frontend:** User clicks "Step".
    *   **Frontend:** Sends `/api/step` request.
    *   **Backend:** Receives request. Executes `Processor.step()` in non-pipelined mode.
    *   **Backend:** Performs **all 5 stages (IF, ID, EX, MEM, WB) sequentially for the single instruction pointed to by the current PC** within this one `step()` call.
        *   Fetches instruction at PC.
        *   Decodes instruction, reads registers.
        *   Executes ALU operation / calculates address / evaluates branch.
        *   Accesses memory (if Load/Store).
        *   Writes back result to register (if applicable).
        *   Calculates the *next* PC value (PC+4 or branch/jump target).
    *   **Backend:** Updates internal state: Register File, Memory (if stored), PC (to the calculated *next* PC).
    *   **Backend:** Increments cycle count (often by 1 per instruction, or more if multi-cycle non-pipelined) and updates other relevant stats (instruction count).
    *   **Backend:** Gathers state for response:
        *   `pc`: The **newly updated** Program Counter.
        *   `registers`: The **complete current state** of the register file (reflecting any write-back from the completed instruction).
        *   `memory_updates`: Any memory location that was written to by a Store instruction.
        *   `stats`: Updated cycle count, instruction count, etc.
        *   `executed_instruction_details`: Info about the instruction that just completed (e.g., its assembly string, address).
        *   **(No pipeline stage data is relevant or sent).**
    *   **Backend:** Sends JSON response.
    *   **Frontend:** Receives response.
    *   **Frontend:** Updates React state:
        *   Updates PC display.
        *   Updates the Register Table view completely.
        *   Updates the Memory View based on `memory_updates`.
        *   Updates the Statistics display.
        *   **(Pipeline diagram component is likely hidden or shows no activity).**

3.  **Loop:**
    *   The process repeats for each click of the "Step" button, executing one full instruction per step. 