Backend Architecture and Control Flow (RISC-V Simulator)

This document details the structure and interaction of the Python backend components for the RISC-V simulator, explaining the control flow for different execution modes.

**I. Backend File Descriptions (`src/` directory):**

1.  **`main.py` (or `app.py`)**
    *   **Purpose:** Entry point for the backend server. Handles API requests from the frontend.
    *   **Key Components:**
        *   Flask/Django application instance.
        *   API endpoint definitions (e.g., `/api/load_code`, `/api/step`, `/api/get_state`).
        *   Instantiates and holds the main `Processor` object.
        *   Handles JSON serialization/deserialization for API communication.
    *   **Interaction:** Receives HTTP requests from the frontend, calls methods on the `Processor` object, formats the processor's state into JSON, and sends HTTP responses back to the frontend.

2.  **`processor.py`**
    *   **Purpose:** The core simulation engine. Orchestrates the execution flow, manages pipeline stages (if applicable), and interacts with other components.
    *   **Key Components:**
        *   `Processor` class.
        *   Internal state: PC (Program Counter), current execution mode (Non-Pipelined, Pipelined Stall, Pipelined Forward).
        *   References to `RegisterFile`, `Memory`, and `HDU` objects.
        *   Pipeline registers/latches (e.g., `if_id_latch`, `id_ex_latch`, `ex_mem_latch`, `mem_wb_latch`) represented as dictionaries or custom objects holding instruction, PC, control signals, intermediate results.
        *   Methods like `load_program()`, `step()`, `run_one_cycle_pipelined()`, `execute_instruction_non_pipelined()`, `get_state()`.
        *   Logic for each pipeline stage (IF, ID, EX, MEM, WB) or sequential execution.
        *   Statistics tracking variables (cycles, instructions, stalls, etc.).
    *   **Interaction:** Uses `Memory` for instruction/data fetch/store. Uses `RegisterFile` for reading/writing registers. Uses `HDU` (in pipelined modes) to get hazard control signals. Is controlled by `main.py` via its methods.

3.  **`memory.py`**
    *   **Purpose:** Simulates the main memory (Instruction and Data).
    *   **Key Components:**
        *   `Memory` class.
        *   Internal data structure (e.g., dictionary, bytearray) to store memory contents, mapping addresses to values.
        *   Methods like `read(address, num_bytes)`, `write(address, value, num_bytes)`, `load_hex_file(file_path)`.
    *   **Interaction:** Accessed by `Processor` during IF (Instruction Fetch), MEM (Load/Store) stages.

4.  **`register_file.py`**
    *   **Purpose:** Simulates the RISC-V general-purpose register file (x0-x31).
    *   **Key Components:**
        *   `RegisterFile` class.
        *   Internal data structure (e.g., list or dictionary) to store the 32 register values.
        *   Methods like `read(register_number)`, `write(register_number, value)`. Ensures `x0` always remains zero.
    *   **Interaction:** Accessed by `Processor` during ID (reading source registers rs1, rs2) and WB (writing destination register rd).

5.  **`hdu.py` (Hazard Detection Unit)**
    *   **Purpose:** Detects data and control hazards in pipelined modes. Generates control signals for stalling and/or forwarding. *This file is largely inactive in non-pipelined mode.*
    *   **Key Components:**
        *   `HDU` class.
        *   Methods like `detect_hazards_stall_only(id_stage, ex_stage, mem_stage, wb_stage)` returning stall signals (e.g., `stall_if`, `stall_id`, `insert_bubble_ex`).
        *   Methods like `detect_hazards_forwarding(id_stage, ex_stage, mem_stage, wb_stage)` returning both stall signals (for Load-Use, control) and forwarding MUX select signals (e.g., `forward_ex_rs1_from`, `forward_ex_rs2_from`).
        *   Logic to compare register numbers (rs1, rs2 in ID vs rd in EX, MEM, WB) based on instruction types and control signals (e.g., `RegWrite` enable).
    *   **Interaction:** Called by `Processor` at the beginning of each cycle in pipelined modes. Takes current pipeline stage information as input and provides control signals back to the `Processor`.

6.  **`utility.py` (or similar)**
    *   **Purpose:** Contains helper functions used across different modules.
    *   **Key Components:** Functions for sign extension, number conversions (binary/hex/decimal), instruction decoding helpers, etc.
    *   **Interaction:** Imported and used by `Processor`, `HDU`, and potentially other modules as needed.

**II. Backend Control Flow by Mode:**

**(A) Non-Pipelined Mode:**

1.  **API Call:** Frontend -> `main.py` (`/api/step`).
2.  **Processor Call:** `main.py` -> `Processor.execute_instruction_non_pipelined()`.
3.  **Sequential Execution (within Processor method):**
    *   IF: `Processor` -> `Memory.read(PC)` -> gets instruction.
    *   ID: `Processor` decodes instruction -> `Processor` -> `RegisterFile.read(rs1/rs2)` -> gets operands.
    *   EX: `Processor` performs ALU logic. For branches/jumps, calculates target PC.
    *   MEM: If Load/Store: `Processor` -> `Memory.read/write(address, data)`.
    *   WB: If register write: `Processor` -> `RegisterFile.write(rd, result)`.
    *   PC Update: `Processor` updates internal PC to next address (PC+4 or target).
4.  **State Return:** `Processor` returns final state (new PC, updated RegFile state, memory changes) -> `main.py`.
5.  **API Response:** `main.py` -> Frontend (JSON).
    *   *`HDU` is not involved.*

**(B) Pipelined Mode (Stalling Only):**

1.  **API Call:** Frontend -> `main.py` (`/api/step`).
2.  **Processor Call:** `main.py` -> `Processor.run_one_cycle_pipelined()`.
3.  **Cycle Simulation (within Processor method):**
    *   **Hazard Check:** `Processor` -> `HDU.detect_hazards_stall_only(pipeline_latches)` -> gets `stall_signals`.
    *   **Stage Logic (Concurrent):** `Processor` executes logic for each stage (WB, MEM, EX, ID, IF), using `stall_signals` to potentially inhibit actions:
        *   WB: `Processor` -> `RegisterFile.write()` (if RegWrite enabled for WB instruction).
        *   MEM: `Processor` -> `Memory.read/write()` (if MemRead/Write enabled for MEM instruction).
        *   EX: `Processor` performs ALU op (if ID wasn't stalled).
        *   ID: `Processor` decodes & `Processor` -> `RegisterFile.read()` (if IF wasn't stalled).
        *   IF: `Processor` -> `Memory.read(PC)` (if IF wasn't stalled).
    *   **Latch Update:** `Processor` updates pipeline latches (e.g., `id_ex_latch`) based on `stall_signals` (pass data forward, hold, or insert NOP).
    *   **PC Update:** `Processor` updates PC based on `stall_signals` and branch/jump results.
4.  **State Return:** `Processor` returns state (PC, RegFile, MEM changes, **pipeline latch contents**, **stall status**) -> `main.py`.
5.  **API Response:** `main.py` -> Frontend (JSON including pipeline/stall info).

**(C) Pipelined Mode (Forwarding + Stalling):**

1.  **API Call:** Frontend -> `main.py` (`/api/step`).
2.  **Processor Call:** `main.py` -> `Processor.run_one_cycle_pipelined()`.
3.  **Cycle Simulation (within Processor method):**
    *   **Hazard Check:** `Processor` -> `HDU.detect_hazards_forwarding(pipeline_latches)` -> gets `stall_signals` (for Load-Use/Control) AND `forwarding_signals`.
    *   **Stage Logic (Concurrent):** `Processor` executes logic for each stage:
        *   WB: `Processor` -> `RegisterFile.write()` (if enabled).
        *   MEM: `Processor` -> `Memory.read/write()` (if enabled).
        *   **EX:** `Processor` performs ALU op. **Crucially, input MUXes select operands based on `forwarding_signals`** (forwarded from EX/MEM or MEM/WB latches, or read from ID/EX latch). Only stalled if Load-Use/Control hazard detected.
        *   ID: `Processor` decodes & `Processor` -> `RegisterFile.read()` (unless stalled).
        *   IF: `Processor` -> `Memory.read(PC)` (unless stalled).
    *   **Latch Update:** `Processor` updates pipeline latches based on `stall_signals`.
    *   **PC Update:** `Processor` updates PC based on `stall_signals` and branch/jump results.
4.  **State Return:** `Processor` returns state (PC, RegFile, MEM changes, pipeline latch contents, stall status, **forwarding path info**) -> `main.py`.
5.  **API Response:** `main.py` -> Frontend (JSON including pipeline/stall/forwarding info).

This provides a comprehensive view of how the backend components interact under different simulation strategies. 