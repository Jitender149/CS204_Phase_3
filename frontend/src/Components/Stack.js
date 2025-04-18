import React, { useState, useEffect } from 'react';
import './Stack.css';
import stackStates from './stack_states.json';
import { Link } from 'react-router-dom';

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
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
            {/* Header */}
            <div className="text-center py-8">
                <h1 className="text-5xl font-bold text-blue-400 mb-2">RISC-V SIMULATOR</h1>
                <p className="text-gray-300 text-lg">Stack Visualization</p>
            </div>

            {/* Navigation Bar */}
            <div className="navBar bg-gray-800 rounded-lg shadow-xl mx-auto max-w-6xl px-4">
                <div className="flex justify-center space-x-4 py-4">
                    <Link to='/'>
                        <button type='button' className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Home</button>
                    </Link>
                    <Link to='/memory'>
                        <button type="button" className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Memory</button>
                    </Link>
                    <Link to='/register'>
                        <button type="button" className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Register</button>
                    </Link>
                    <Link to='/dataHazard'>
                        <button type="button" className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Data Hazards</button>
                    </Link>
                    <Link to='/simulator'>
                        <button type='button' className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Simulation</button>
                    </Link>
                    <Link to='/stack'>
                        <button type='button' className="px-6 py-2 bg-yellow-600 hover:bg-yellow-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Stack</button>
                    </Link>
                    <Link to='/branch-prediction'>
                    <button type='button' className="px-6 py-2 bg-pink-600 hover:bg-pink-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105">Branch</button>
                    </Link>
                </div>
            </div>

            {/* Stack Visualization */}
            <div className="max-w-6xl mx-auto px-4 mt-8">
                <div className="bg-gray-800 rounded-lg shadow-xl p-8">
                    <div className="stack-container">
                        <div className="controls">
                            <button 
                                onClick={handlePreviousCycle}
                                disabled={currentCycle === 0}
                                className="cycle-button"
                            >
                                Previous Cycle
                            </button>
                            <span className="cycle-counter">Cycle: {currentCycle}</span>
                            <button 
                                onClick={handleNextCycle}
                                disabled={currentCycle === maxCycle}
                                className="cycle-button"
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
                </div>
            </div>
        </div>
    );
};

export default Stack; 