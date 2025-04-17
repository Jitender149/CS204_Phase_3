import React from 'react'
import './MemoryScreen.css'
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { Link } from 'react-router-dom'
import MemoryTable from './MemoryTable.js'

const MemoryScreen = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold text-blue-400 mb-2">RISC-V SIMULATOR</h1>
        <p className="text-gray-300 text-lg">Memory Visualization</p>
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
        </div>
      </div>

      {/* Memory Table Section */}
      <div className="max-w-6xl mx-auto px-4 mt-8">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <MemoryTable />
        </div>
      </div>
    </div>
  )
}

export default MemoryScreen
