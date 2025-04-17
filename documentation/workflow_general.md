General Project Workflow (RISC-V Simulator)

This document outlines the typical flow of execution and interaction within the RISC-V simulator project, involving both the frontend user interface and the backend processor simulation logic.

1.  **Initialization:**
    *   The user launches the application.
    *   The frontend UI (React) is rendered in the browser.
    *   The backend simulation engine (Python) is ready to receive commands or code.

2.  **Code Input:**
    *   The user inputs RISC-V assembly code or loads a pre-compiled binary/hex file via the frontend interface (e.g., the input screen).

3.  **Backend Processing Setup:**
    *   The frontend sends the input code/file content to the backend API endpoint.
    *   The backend receives the code. If it's assembly, it likely assembles it into machine code (or uses an intermediate representation). If it's hex/binary, it loads it directly into the simulated memory.
    *   The backend initializes the simulated processor state:
        *   Program Counter (PC) set to the starting address.
        *   Registers initialized (usually to zero).
        *   Memory loaded with the program instructions and any initial data.
        *   Pipeline stages (if applicable) initialized (often stalled initially).
        *   Statistics counters reset.

4.  **Simulation Execution Loop (Controlled by Frontend):**
    *   The user interacts with the simulation controls on the frontend (e.g., "Step", "Run", "Prev").
    *   **Step Command:**
        *   Frontend sends a "step" request to the backend (requesting simulation for one clock cycle).
        *   Backend simulates one clock cycle according to the currently selected mode (Non-Pipelined, Pipelined without Forwarding, Pipelined with Forwarding).
        *   This involves fetching, decoding, executing instructions, handling hazards/stalls/forwarding, accessing memory, and writing back results.
        *   The backend updates the internal processor state (PC, registers, memory, pipeline latches).
        *   Statistics (CPI, cycles, hazards, stalls, etc.) are updated.
        *   Backend sends the *complete updated state* back to the frontend. This includes:
            *   Current register values.
            *   Relevant memory sections.
            *   Contents of each pipeline stage/latch for visualization.
            *   Forwarding paths used (if applicable).
            *   Stall status.
            *   Updated statistics.
            *   Current instruction details (if available).
        *   Frontend receives the state data and updates the UI components (Register Table, Memory View, Pipeline Diagram, Statistics Display).
    *   **Prev Command:** (If implemented)
        *   Frontend sends a "prev" request.
        *   Backend needs to revert to the *previous* cycle's state. This often requires storing simulation history or having a reversible simulation mechanism.
        *   Backend sends the restored previous state to the frontend.
        *   Frontend updates the UI.
    *   **Run Command:** (If implemented)
        *   Frontend sends a "run" request.
        *   Backend runs the simulation continuously until a breakpoint, halt instruction, or error occurs. It might send state updates periodically or only upon completion/pause.

5.  **Output and Visualization:**
    *   The frontend continuously displays the state received from the backend.
    *   The pipeline diagram visually represents the instructions flowing through the stages, highlighting stalls, forwarded data paths, and active stages.
    *   Register and memory views allow the user to inspect the processor's state.
    *   Statistics provide performance insights.

6.  **Termination:**
    *   The simulation ends when a halt instruction is executed, an error occurs, or the user stops the process.
    *   Final statistics and state are displayed. 