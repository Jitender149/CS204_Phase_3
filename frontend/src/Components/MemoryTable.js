import { useEffect, useState } from "react";
import MemoryData from './data.json'
import './MemoryScreen.css'

function MemoryTable() {
  const [hoveredIndex, setHoveredIndex] = useState(null)
  const [value1, setValue1] = useState(null)
  const [value2, setValue2] = useState(null)
  const [value3, setValue3] = useState(null)
  const [value4, setValue4] = useState(null)

  const handleMouseEnter = (index, value) => {
    setHoveredIndex(index);
    if(value == 1){
      setValue1(true)
      setValue2(false)
      setValue3(false)
      setValue4(false)
    }
    else if(value == 2){
      setValue1(false)
      setValue2(true)
      setValue3(false)
      setValue4(false)
    }
    else if(value == 3){
      setValue1(false)
      setValue2(false)
      setValue3(true)
      setValue4(false)
    }
    else {
      setValue1(false)
      setValue2(false)
      setValue3(false)
      setValue4(true)
    }
  };

  const handleMouseLeave = () => {
    setHoveredIndex(null);
    setValue1(false)
    setValue2(false)
    setValue3(false)
    setValue4(false)
  };

  return (
    <div style={{ backgroundColor: 'transparent' }}>
      <table className="table" style={{ backgroundColor: 'transparent' }}>
        <thead>
          <tr>
            <th style={{ width: '25%', textAlign: 'center', color: '#ffffff', backgroundColor: '#3a3a3a', padding: '1rem' }}>Memory</th>
            <th style={{ width: '25%', textAlign: 'center', color: '#ffffff', backgroundColor: '#3a3a3a', padding: '1rem' }}>Hex</th>
            <th style={{ width: '25%', textAlign: 'center', color: '#ffffff', backgroundColor: '#3a3a3a', padding: '1rem' }}>Binary</th>
            <th style={{ width: '25%', textAlign: 'center', color: '#ffffff', backgroundColor: '#3a3a3a', padding: '1rem' }}>Decimal</th>
          </tr>
        </thead>
        <tbody>
          {MemoryData.map((data, index) => {
            if(index > 300) return null;
            return (
              <tr key={index}>
                <td 
                  style={{ 
                    width: '25%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value1 ? "#4a4a4a" : "transparent"
                  }}
                  onMouseEnter={() => handleMouseEnter(index, 1)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['memory']}
                </td>
                <td 
                  style={{ 
                    width: '25%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value2 ? "#4a4a4a" : "transparent"
                  }}
                  onMouseEnter={() => handleMouseEnter(index, 2)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['hex']}
                </td>
                <td 
                  style={{ 
                    width: '25%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value3 ? "#4a4a4a" : "transparent"
                  }}
                  onMouseEnter={() => handleMouseEnter(index, 3)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['binary']}
                </td>
                <td 
                  style={{ 
                    width: '25%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value4 ? "#4a4a4a" : "transparent"
                  }}
                  onMouseEnter={() => handleMouseEnter(index, 4)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['decimal']}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  )
}

export default MemoryTable