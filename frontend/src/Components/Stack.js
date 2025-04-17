import React, { useState, useEffect } from 'react';
import './Stack.css';
import stackStates from './stack_states.json';

const Stack = () => {
    const [currentCycle, setCurrentCycle] = useState(0);
    const [currentStack, setCurrentStack] = useState([]);
    const [maxCycle, setMaxCycle] = useState(0);
    
    useEffect(() => {
        // Find the maximum cycle number
        if (stackStates.length > 0) {
            setMaxCycle(stackStates[stackStates.length - 1].cycle);
        }
    }, []);

    useEffect(() => {
        // Find the stack state for the current cycle
        const stackState = stackStates.find(state => state.cycle === currentCycle);
        if (stackState) {
            setCurrentStack(stackState.stack);
        } else {
            setCurrentStack([]);
        }
    }, [currentCycle]);
    
    const handlePreviousCycle = () => {
        setCurrentCycle(prev => Math.max(0, prev - 1));
    };

    const handleNextCycle = () => {
        setCurrentCycle(prev => Math.min(maxCycle, prev + 1));
    };
    
    return (
        <div className="stack-container">
            <h2>Call Stack</h2>
            <div className="controls">
                <button 
                    onClick={handlePreviousCycle}
                    disabled={currentCycle === 0}
                >
                    Previous Cycle
                </button>
                <span>Cycle: {currentCycle}</span>
                <button 
                    onClick={handleNextCycle}
                    disabled={currentCycle === maxCycle}
                >
                    Next Cycle
                </button>
            </div>
            <div className="stack-visualization">
                {currentStack.length === 0 ? (
                    <div className="empty-stack">Stack is empty</div>
                ) : (
                    currentStack.map((entry, index) => (
                        <div key={index} className="stack-entry">
                            <div className="stack-level">Stack Level {index}</div>
                            <div className="instruction-type">Type: {entry.instruction_type}</div>
                            <div className="return-address">Return Address: 0x{entry.return_address.toString(16).padStart(8, '0')}</div>
                            <div className="pc">PC: 0x{entry.pc.toString(16).padStart(8, '0')}</div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Stack; 