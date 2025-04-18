import React from 'react'
import './BranchPrediction.css'
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { Link } from 'react-router-dom'
import branchData from './branch_prediction.json'

const BranchPrediction = () => {
  // Validate and format the data
  const formatHex = (value) => {
    if (value === undefined || value === null) return 'N/A';
    return `0x${value.toString(16)}`;
  };

  const formatPrediction = (prediction) => {
    if (!prediction) return 'N/A';
    return prediction;
  };

  const formatResult = (misprediction) => {
    if (misprediction === undefined || misprediction === null) return 'N/A';
    return misprediction ? 'Misprediction' : 'Correct';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-5xl font-bold text-blue-400 mb-2">RISC-V SIMULATOR</h1>
        <p className="text-gray-300 text-lg">Branch Prediction Analysis</p>
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

      {/* Statistics Section */}
      <div className="max-w-6xl mx-auto px-4 mt-8">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-blue-400 mb-4">Branch Prediction Statistics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-700 p-4 rounded-lg">
              <div className="text-gray-400">Total Branches</div>
              <div className="text-xl font-semibold">{branchData?.total_branches || 0}</div>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg">
              <div className="text-gray-400">Correct Predictions</div>
              <div className="text-xl font-semibold">{branchData?.correct_predictions || 0}</div>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg">
              <div className="text-gray-400">Mispredictions</div>
              <div className="text-xl font-semibold">{branchData?.mispredictions || 0}</div>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg">
              <div className="text-gray-400">Prediction Accuracy</div>
              <div className="text-xl font-semibold">
                {branchData?.total_branches 
                  ? `${((branchData.correct_predictions / branchData.total_branches) * 100).toFixed(2)}%`
                  : '0%'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Predictions Section */}
      <div className="max-w-6xl mx-auto px-4 mt-8 mb-8">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-blue-400 mb-4">Detailed Branch Predictions</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-700">
                  <th className="px-4 py-2">PC</th>
                  <th className="px-4 py-2">Instruction</th>
                  <th className="px-4 py-2">Prediction</th>
                  <th className="px-4 py-2">Actual</th>
                  <th className="px-4 py-2">Target Address</th>
                  <th className="px-4 py-2">Result</th>
                </tr>
              </thead>
              <tbody>
                {branchData?.predictions?.map((prediction, index) => (
                  <tr key={index} className="border-b border-gray-700">
                    <td className="px-4 py-2">{formatHex(prediction.pc)}</td>
                    <td className="px-4 py-2">{formatPrediction(prediction.instruction)}</td>
                    <td className="px-4 py-2">{formatPrediction(prediction.prediction)}</td>
                    <td className="px-4 py-2">{formatPrediction(prediction.actual)}</td>
                    <td className="px-4 py-2">{formatHex(prediction.target)}</td>
                    <td className={`px-4 py-2 ${prediction.misprediction ? 'text-red-400' : 'text-green-400'}`}>
                      {formatResult(prediction.misprediction)}
                    </td>
                  </tr>
                )) || (
                  <tr>
                    <td colSpan="6" className="text-center py-4 text-gray-400">
                      No branch prediction data available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default BranchPrediction 