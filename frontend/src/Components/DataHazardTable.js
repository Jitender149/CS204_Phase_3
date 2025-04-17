import { useEffect, useState } from "react";
// import RegisterData from "./RegisterData.js";
import RegisterData from './cycle.json'
import './DataHazardScreen.css'

function DataHazardTable(){

const [hoveredIndex, setHoveredIndex] = useState(null)
const [value1, setValue1] = useState(null)
const [value2, setValue2] = useState(null)
const [value3, setValue3] = useState(null)
const [value4, setValue4] = useState(null)
const [value5, setValue5] = useState(null)

const handleMouseEnter = (index, value) => {
  setHoveredIndex(index);
  if(value == 1){
    setValue1(true)
    setValue2(false)
    setValue3(false)
    setValue4(false)
    setValue5(false)
}
else if(value == 2){
    setValue1(false)
    setValue2(true)
    setValue3(false)
    setValue4(false)
    setValue5(false)
}
else if(value == 3){
    setValue1(false)
    setValue2(false)
    setValue3(true)
    setValue4(false)
    setValue5(false)
}
else if(value == 4){
    setValue1(false)
    setValue2(false)
    setValue3(false)
    setValue4(true)
    setValue5(false)
  }
  else{
    setValue1(false)
    setValue2(false)
    setValue3(false)
    setValue4(false)
    setValue5(true)
  }
};


const handleMouseLeave = () => {
  setHoveredIndex(null);
  setValue1(false)
  setValue2(false)
  setValue3(false)
  setValue4(false)
  setValue5(false)
};


// get table column
 const column = Object.keys(RegisterData[0]);

 // get table heading data
 const ThData =()=>{
    
     return column.reverse().map((data)=>{
        //  return <th key={data} style={{width:'20%', textAlign:'center'}}>{data}</th>
        if(data != 'id' && data != 'forwarding' && data != 'value'){
            return <th style={{width:'20%', textAlign:'center', color: '#ffffff', backgroundColor: '#3a3a3a', padding: '1rem'}}>{data}</th>
        }
     })
    // return <div style={{width:'100%', display:'flex'}}>
    //     <th style={{width:'20%', textAlign:'center'}}>{column[5]}</th>
    //     <th style={{width:'20%', textAlign:'center'}}>{column[4]}</th>
    //     <th style={{width:'20%', textAlign:'center'}}>{column[3]}</th>
    //     <th style={{width:'20%', textAlign:'center'}}>{column[2]}</th>
    //     <th style={{width:'20%', textAlign:'center'}}>{column[1]}</th>
    // </div>
 }
// get table row data

function func(index) {
    return RegisterData[index]['forwarding']
}

const tdData =() =>{
   
     return RegisterData.map((data,index)=>{
        if(index > 300) return
       return(
           <tr >
                {/* {
                   column.map((v)=>{
                       return <td style={{width:'20%', textAlign:'center'}}>{data[v]}</td>
                   })
                } */}
                
                <td 
                  style={{ 
                    width: '20%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value1 ? "#4a4a4a" : "transparent",
                    whiteSpace: 'normal',
                    wordWrap: 'break-word'
                  }}
                  onMouseEnter={() => handleMouseEnter(index,1)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['fetch']}
                  {data['forwarding'] == 4 && data['value'] && (
                    <div style={{ 
                      color: '#4CAF50', 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)',
                      padding: '0.5rem',
                      borderRadius: '4px',
                      marginTop: '0.5rem',
                      fontSize: '0.8rem'
                    }}>
                      {data['value']}
                    </div>
                  )}
                </td>
                <td 
                  style={{ 
                    width: '20%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value2 ? "#4a4a4a" : "transparent",
                    whiteSpace: 'normal',
                    wordWrap: 'break-word'
                  }}
                  onMouseEnter={() => handleMouseEnter(index,2)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['decode']}
                  {data['forwarding'] == 3 && data['value'] && (
                    <div style={{ 
                      color: '#4CAF50', 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)',
                      padding: '0.5rem',
                      borderRadius: '4px',
                      marginTop: '0.5rem',
                      fontSize: '0.8rem'
                    }}>
                      {data['value']}
                    </div>
                  )}
                </td>
                <td 
                  style={{ 
                    width: '20%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value3 ? "#4a4a4a" : "transparent",
                    whiteSpace: 'normal',
                    wordWrap: 'break-word'
                  }}
                  onMouseEnter={() => handleMouseEnter(index,3)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['execute']}
                  {data['forwarding'] == 2 && data['value'] && (
                    <div style={{ 
                      color: '#4CAF50', 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)',
                      padding: '0.5rem',
                      borderRadius: '4px',
                      marginTop: '0.5rem',
                      fontSize: '0.8rem'
                    }}>
                      {data['value']}
                    </div>
                  )}
                </td>
                <td 
                  style={{ 
                    width: '20%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value4 ? "#4a4a4a" : "transparent",
                    whiteSpace: 'normal',
                    wordWrap: 'break-word'
                  }}
                  onMouseEnter={() => handleMouseEnter(index,4)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['memory']}
                  {data['forwarding'] == 1 && data['value'] && (
                    <div style={{ 
                      color: '#4CAF50', 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)',
                      padding: '0.5rem',
                      borderRadius: '4px',
                      marginTop: '0.5rem',
                      fontSize: '0.8rem'
                    }}>
                      {data['value']}
                    </div>
                  )}
                </td>
                <td 
                  style={{ 
                    width: '20%', 
                    textAlign: 'center', 
                    color: '#e0e0e0',
                    padding: '1rem',
                    backgroundColor: hoveredIndex === index && value5 ? "#4a4a4a" : "transparent",
                    whiteSpace: 'normal',
                    wordWrap: 'break-word'
                  }}
                  onMouseEnter={() => handleMouseEnter(index,5)} 
                  onMouseLeave={handleMouseLeave}
                >
                  {data['writeback']}
                  {data['forwarding'] == 0 && data['value'] && (
                    <div style={{ 
                      color: '#4CAF50', 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)',
                      padding: '0.5rem',
                      borderRadius: '4px',
                      marginTop: '0.5rem',
                      fontSize: '0.8rem'
                    }}>
                      {data['value']}
                    </div>
                  )}
                </td>
           </tr>
       )
     })
}

const renderCellContent = (stage, value, forwardingValue, targetValue) => (
  <div className="cell-content">
    <div className="stage-value">{stage}</div>
    {forwardingValue === targetValue && value && (
      <div className="forwarding-value">{value}</div>
    )}
  </div>
);

  return (
      <div style={{ backgroundColor: 'transparent' }}>
        <table className="table" style={{ backgroundColor: 'transparent' }}>
        <thead>
         <tr>{ThData()}</tr>
        </thead>
        <tbody>
        {tdData()}
        </tbody>
       </table>
      </div>
  )
}
export default DataHazardTable;