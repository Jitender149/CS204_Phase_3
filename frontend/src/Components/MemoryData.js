import React, { useState, useEffect } from 'react';
import './MemoryScreen.css';

const MemoryData = () => {
  const [memoryData, setMemoryData] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/memory')
      .then(response => response.json())
      .then(data => setMemoryData(data))
      .catch(error => console.error('Error fetching memory data:', error));
  }, []);

  const handleAddressClick = (address) => {
    setSelectedAddress(address);
  };

  return (
    <div className="memory-data-container">
      <div className="memory-data-header">
        <h2 className="text-2xl font-bold text-blue-400 mb-4">Memory Data</h2>
        <div className="memory-data-filters">
          <input
            type="text"
            placeholder="Search address..."
            className="bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      
      <div className="memory-data-content">
        {memoryData.map((item, index) => (
          <div
            key={index}
            className={`memory-data-item ${
              selectedAddress === item.address ? 'bg-blue-900' : 'bg-gray-800'
            } hover:bg-gray-700 transition-colors duration-200`}
            onClick={() => handleAddressClick(item.address)}
          >
            <div className="memory-data-address">
              <span className="text-blue-400">Address:</span>
              <span className="font-mono">{item.address}</span>
            </div>
            <div className="memory-data-value">
              <span className="text-blue-400">Value:</span>
              <span className="font-mono">{item.value}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MemoryData;