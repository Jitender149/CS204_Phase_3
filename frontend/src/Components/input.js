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
        <>
            <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <label className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Upload File
        <input
          type="file"
          className="hidden"
          accept=".txt,.mc"
          onChange={handleFileInput}
        />
      </label>
      {selectedFile && <p>{selectedFile.name}</p>}
                <div className="flex flex-col w-full space-y-2 mb-8">
                    
                    <label className="text-2xl font-bold">Options:</label>
                    
                    <div className="flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={pipeliningEnabled}
                        onChange={handlePipeliningEnabled}
                    />
                    <label className="text-lg font-medium">Enable pipelining</label>
                    </div>
                    <div className="flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={forwardingEnabled}
                        onChange={handleForwardingEnabled}
                    />
                    <label className="text-lg font-medium">Enable forwarding</label>
                    </div>
                    <div className="flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printRegistersEachCycle}
                        onChange={handlePrintRegistersEachCycle}
                    />
                    <label className="text-lg font-medium">Enable printing registers in each cycle</label>
                    </div>
                    <div className="flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printPipelineRegisters}
                        onChange={handlePrintPipelineRegisters}
                    />
                    <label className="text-lg font-medium">Enable printing pipeline registers</label>
                    </div>
                    <div className="flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printSpecificPipelineRegisters}
                        onChange={handlePrintSpecificPipelineRegisters}
                    />
                    <label className="text-lg font-medium">Enable printing specific pipeline registers</label>
                    {
                        printSpecificPipelineRegisters && (
                            <>
                            <input
                                type="number"
                                id="number-input"
                                value={instructionNumber}
                                onChange={handleInstructionNumber}
                                required
                            />
                            <label className="text-lg font-medium">Enter the number</label>
                            </>
                        )
                    }
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={handleSubmit}>
                        Submit
                    </button>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Input;