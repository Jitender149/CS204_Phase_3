import React, {useState} from "react";

function Input() {
    const [pipeliningEnabled, setPipeliningEnabled] = useState(false);
    const [forwardingEnabled, setForwardingEnabled] = useState(false);
    const [printRegistersEachCycle, setPrintRegistersEachCycle] = useState(false);
    const [printPipelineRegisters, setPrintPipelineRegisters] = useState(false);
    const [printSpecificPipelineRegisters, setPrintSpecificPipelineRegisters] = useState(false);
    const [instructionNumber, setInstructionNumber] = useState(-1);
    const [selectedFile, setSelectedFile] = useState(null);
    
        function handleFileInput(e) {
          setSelectedFile(e.target.files[0]);
        };

    const handlePipeliningEnabled = () => {
        setPipeliningEnabled(!pipeliningEnabled);
    };

    const handleForwardingEnabled = () => {
        setForwardingEnabled(!forwardingEnabled);
    };

    const handlePrintRegistersEachCycle = () => {
        setPrintRegistersEachCycle(!printRegistersEachCycle);
    };

    const handlePrintPipelineRegisters = () => {
        setPrintPipelineRegisters(!printPipelineRegisters);
    };

    const handlePrintSpecificPipelineRegisters = () => {
        setPrintSpecificPipelineRegisters(!printSpecificPipelineRegisters);
    };

    const handleInstructionNumber = (event) => {
        setInstructionNumber(event.target.value);
    };

    const handleSubmit = () => {
        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('pipelining_enabled', pipeliningEnabled);
        formData.append('forwarding_enabled', forwardingEnabled);
        formData.append('print_registers_each_cycle', printRegistersEachCycle);
        formData.append('print_pipeline_registers', printPipelineRegisters);
        // formData.append('print_specific_pipeline_registers', [printSpecificPipelineRegisters, instructionNumber]);  
        formData.append('print_specific_pipeline_registers',printSpecificPipelineRegisters);
        if(instructionNumber != null) formData.append('number',instructionNumber);
        else formData.append('number',0);
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(
            fetch('http://127.0.0.1:5000/runScripts',{
                method: 'POST',
                body: JSON.stringify('Hello')
            })
            .then(() => {
                console.log('Successfully returned after running both files')
                window.location = 'http://localhost:3000/memory'
            })
            .catch(error => console.log(error))
        )
        .catch(error => console.error(error));
    };
    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
            {/* Header */}
            <div className="text-center py-8">
                <h1 className="text-5xl font-bold text-blue-400 mb-2">RISC-V SIMULATOR</h1>
                <p className="text-gray-300 text-lg">A Pipeline Simulation Tool</p>
            </div>

            {/* Main Content */}
            <div className="max-w-4xl mx-auto px-4">
                <div className="bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
                    {/* File Upload Section */}
                    <div className="mb-8 text-center">
                        <label className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg cursor-pointer transition duration-300 transform hover:scale-105">
                            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                            </svg>
                            Upload RISC-V Code
                            <input
                                type="file"
                                className="hidden"
                                accept=".txt,.mc"
                                onChange={handleFileInput}
                            />
                        </label>
                        {selectedFile && (
                            <p className="mt-4 text-green-400 font-medium">
                                Selected: {selectedFile.name}
                            </p>
                        )}
                    </div>

                    {/* Options Section */}
                    <div className="space-y-6">
                        <h2 className="text-2xl font-bold text-blue-400 mb-4">Simulation Options</h2>
                        
                        {/* Pipelining Option */}
                        <div className="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition duration-300">
                            <input
                                type="checkbox"
                                className="h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                                checked={pipeliningEnabled}
                                onChange={handlePipeliningEnabled}
                            />
                            <label className="ml-3 text-lg font-medium">Enable Pipelining</label>
                        </div>

                        {/* Forwarding Option */}
                        <div className="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition duration-300">
                            <input
                                type="checkbox"
                                className="h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                                checked={forwardingEnabled}
                                onChange={handleForwardingEnabled}
                            />
                            <label className="ml-3 text-lg font-medium">Enable Forwarding</label>
                        </div>

                        {/* Register Printing Options */}
                        <div className="space-y-4">
                            <div className="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition duration-300">
                                <input
                                    type="checkbox"
                                    className="h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                                    checked={printRegistersEachCycle}
                                    onChange={handlePrintRegistersEachCycle}
                                />
                                <label className="ml-3 text-lg font-medium">Print Registers Each Cycle</label>
                            </div>

                            <div className="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition duration-300">
                                <input
                                    type="checkbox"
                                    className="h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                                    checked={printPipelineRegisters}
                                    onChange={handlePrintPipelineRegisters}
                                />
                                <label className="ml-3 text-lg font-medium">Print Pipeline Registers</label>
                            </div>

                            <div className="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition duration-300">
                                <input
                                    type="checkbox"
                                    className="h-5 w-5 text-blue-500 rounded focus:ring-blue-400"
                                    checked={printSpecificPipelineRegisters}
                                    onChange={handlePrintSpecificPipelineRegisters}
                                />
                                <label className="ml-3 text-lg font-medium">Print Specific Pipeline Registers</label>
                            </div>

                            {/* Instruction Number Input */}
                            {printSpecificPipelineRegisters && (
                                <div className="ml-8 p-4 bg-gray-600 rounded-lg">
                                    <input
                                        type="number"
                                        id="number-input"
                                        value={instructionNumber}
                                        onChange={handleInstructionNumber}
                                        className="w-full px-4 py-2 bg-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        placeholder="Enter instruction number"
                                        required
                                    />
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Submit Button */}
                    <div className="mt-8 text-center">
                        <button
                            onClick={handleSubmit}
                            className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                            Start Simulation
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Input;