import { useEffect, useState } from "react";
// import RegisterData from "./RegisterData.js";
import RegisterData from './cycle.json'

function DataHazardTable(){

const [hoverdIndex, setHoverdIndex] = useState(null)
const [value1, setValue1] = useState(null)
const [value2, setValue2] = useState(null)
const [value3, setValue3] = useState(null)
const [value4, setValue4] = useState(null)
const [value5, setValue5] = useState(null)

const handleMouseEnter = (index, value) => {
  setHoverdIndex(index);
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


const handleMouseLeave = (value) => {
  setHoverdIndex(null);
  setValue1(false)
  setValue2(false)
  setValue3(false)
  setValue4(false)
};


// get table column
 const column = Object.keys(RegisterData[0]);

 // get table heading data
 const ThData =()=>{
    
     return column.reverse().map((data)=>{
        //  return <th key={data} style={{width:'20%', textAlign:'center'}}>{data}</th>
        if(data != 'id' && data != 'forwarding' && data != 'value'){
            return <th style={{width:'20%', textAlign:'center'}}>{data}</th>
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
                
                <td onMouseEnter={() => handleMouseEnter(index,1)} onMouseLeave={() => handleMouseLeave(1)} style={{width:'20%', textAlign:'center', backgroundColor : hoverdIndex == index && value1 ? "#DCCAE9" : "white" }}>{data['fetch']}{func(index) == 4 ? data['value'] : <span></span>}</td>
                <td onMouseEnter={() => handleMouseEnter(index,2)} onMouseLeave={() => handleMouseLeave(2)} style={{width:'20%', textAlign:'center', backgroundColor : hoverdIndex == index && value2 ? "#DCCAE9" : "white"}}>{data['decode']}{func(index) == 3 ? data['value'] : <span></span>}</td>
                <td onMouseEnter={() => handleMouseEnter(index,3)} onMouseLeave={() => handleMouseLeave(3)} style={{width:'20%', textAlign:'center', backgroundColor : hoverdIndex == index && value3 ? "#DCCAE9" : "white"}}>{data['execute']}{func(index) == 2 ? data['value'] : <span></span>}</td>
                <td onMouseEnter={() => handleMouseEnter(index,4)} onMouseLeave={() => handleMouseLeave(4)} style={{width:'20%', textAlign:'center', backgroundColor : hoverdIndex == index && value4 ? "#DCCAE9" : "white  "}}>{data['memory']}{func(index) == 1 ? data['value'] : <span></span>}</td>
                <td onMouseEnter={() => handleMouseEnter(index,5)} onMouseLeave={() => handleMouseLeave(5)} style={{width:'20%', textAlign:'center', backgroundColor : hoverdIndex == index && value5 ? "#DCCAE9" : "white  "}}>{data['writeback']}{func(index) == 0 ? data['value'] : <span></span>}</td>

           </tr>
       )
     })
}
  return (
      <table className="table">
        <thead>
         <tr>{ThData()}</tr>
        </thead>
        <tbody>
        {tdData()}
        </tbody>
       </table>
  )
}
export default DataHazardTable;