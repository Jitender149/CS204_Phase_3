import React from 'react'
import './App.css';
import MemoryScreen from './Components/MemoryScreen.js'
import RegisterScreen from './Components/RegisterScreen.js';
import DataHazardScreen from './Components/DataHazardScreen';
import Simulator from './Components/Simulator.js'
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Input from './Components/input.js'

const App = () => {
  return (
    <div className='App'>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Input />} />
        <Route path='/memory' element={<MemoryScreen />} />
        <Route path='/register' element={<RegisterScreen />} />
        <Route path='/dataHazard' element={<DataHazardScreen />} />
        <Route path='/simulator' element={<Simulator />} />
      </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
