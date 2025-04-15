import { useEffect, useState } from 'react'
import './Simulator.css'
import data from './cycle.json'
import stats from './stats.json'
import { Link } from 'react-router-dom'
const Simulator = () => {

    const [index, setIndex] = useState(0)
    const [value, setValue] = useState(-1)
    useEffect(() => {
        if (data[index]['fetch'] == -1) {
            document.querySelector('.div1').classList.add('glow')
        }
        else {
            document.querySelector('.div1').classList.remove('glow')
        }

        if (data[index]['decode'] == -1) {
            document.querySelector('.div2').classList.add('glow')
        }
        else {
            document.querySelector('.div2').classList.remove('glow')
        }

        if (data[index]['execute'] == -1) {
            document.querySelector('.div3').classList.add('glow')
        }
        else {
            document.querySelector('.div3').classList.remove('glow')
        }

        if (data[index]['memory'] == -1) {
            document.querySelector('.div4').classList.add('glow')
        }
        else {
            document.querySelector('.div4').classList.remove('glow')
        }

        if (data[index]['writeback'] == -1) {
            document.querySelector('.div5').classList.add('glow')
        }
        else {
            document.querySelector('.div5').classList.remove('glow')
        }


        if (data[index]["forwarding"] != -1) {
            if (data[index]['forwarding'] == 0) {
                console.log(1)
                setValue(4);
                let divElement = document.createElement('div');
                divElement.textContent = data[index]["value"];
                divElement.className = 'newDiv'
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
                document.querySelector('.div5').appendChild(divElement)
            }
            else if (data[index]['forwarding'] == 1) {
                setValue(3);
                console.log(1)
                let divElement = document.createElement('div');
                divElement.textContent = data[index]["value"];
                divElement.className = 'newDiv'
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
                document.querySelector('.div4').appendChild(divElement)
            }
            else if (data[index]['forwarding'] == 2) {
                setValue(2);
                console.log(3)
                let divElement = document.createElement('div');
                divElement.textContent = data[index]["value"];
                divElement.className = 'newDiv'
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
                document.querySelector('.div3').appendChild(divElement)
            }
            else if (data[index]['forwarding'] == 3) {
                setValue(1);
                console.log(4)
                let divElement = document.createElement('div');
                divElement.textContent = data[index]["value"];
                divElement.className = 'newDiv'
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
                document.querySelector('.div2').appendChild(divElement)
            }
            else if (data[index]['forwarding'] == 4) {
                setValue(0)
                console.log(5)
                let divElement = document.createElement('div');
                divElement.textContent = data[index]["value"];
                divElement.className = 'newDiv'
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
                document.querySelector('.div1').appendChild(divElement)
            }
            else {
                console.log("HELLO")
                setValue(-1)
                let elt = document.querySelector('.newDiv')
                if(elt !== null) elt.remove()
            }
        }
        else{
            console.log("PRINT")
            let elt = document.querySelector('.newDiv')
            if(elt !== null) elt.remove()
        }

    }, [index])

    function stepHandler() {
        if (index < data.length) setIndex(index + 1)
    }

    function prevHandler() {
        if (index >= 1) setIndex(index - 1)
    }


    return (
        <>
            <div className="complete" style={{height:'100vh'}}>
                <div className='box'>
                    <Link to='/register'>
                        <button type="button" class="btn btn-outline-secondary" style={{ paddingLeft: '30px', paddingRight: '30px' }}>Back</button>
                    </Link>
                    <div className='topbar'>
                        Simulator
                    </div>
                </div>
                <div className='runButtons'>
                    <button type="button" class="btn btn-outline-danger" style={{ marginRight: '40px', paddingLeft: '50px', paddingRight: '50px' }} onClick={stepHandler}>Step</button>
                    <button type="button" class="btn btn-outline-danger" style={{ paddingLeft: '50px', paddingRight: '50px' }} onClick={prevHandler}>Prev</button>
                </div>
                <div className='outer'>
                    <div className='inner div1'>
                        <div className='data1'  style={{ width: '100%' }}><b>{data[index]['fetch']}</b></div>
                        {/* {value == 0 ? <div style={{width:'100%'}}><b>{data[index]['value']}</b></div> : <div></div>} */}
                    </div>
                    <div className='inner div2'>
                        <div className='data2' style={{ width: '100%' }}><b>{data[index]['decode']}</b></div>
                        {/* {value == 1 ? <div style={{ width: '100%' }}><b>{data[index]['value']}</b></div> : <div></div>} */}
                    </div>
                    <div className='inner div3'>
                        <div className='data3' style={{ width: '100%' }}><b>{data[index]['execute']}</b></div>
                        {/* {value == 2 ? <div style={{ width: '100%' }}><b>{data[index]['value']}</b></div> : <div></div>} */}
                    </div>
                    <div className='inner div4'>
                        <div className='data4' style={{ width: '100%' }}><b>{data[index]['memory']}</b></div>
                        {/* {value == 3 ? <div style={{ width: '100%' }}><b>{data[index]['value']}</b></div> : <div></div>} */}
                    </div>
                    <div className='inner div5'>
                        <div className='data5' style={{ width: '100%' }}><b>{data[index]['writeback']}</b></div>
                        {/* {value == 4 ? <div style={{ width: '100%' }}><b>{data[index]['value']}</b></div> : <div></div>} */}
                    </div>
                </div>

                <div className='statistics'>
                    {/* {
                    stats.map((value) => {
                        return <div className='divInner'><b>{value["stats"]}</b>: {value["value"]}</div>
                    })
                } */}
                    <div className='divInner'><b>{stats[0]['stats']}</b>: {stats[0]['value']}</div>
                    <div className='divInner'><b>{stats[1]['stats']}</b>: {stats[1]['value']}</div>
                    <div className='divInner'><b>{stats[2]['stats']}</b>: {stats[2]['value']}</div>
                    <div className='divInner'><b>{stats[3]['stats']}</b>: {stats[3]['value']}</div>
                    <div className='divInner'><b>{stats[4]['stats']}</b>: {stats[4]['value']}</div>
                    <div className='divInner'><b>{stats[5]['stats']}</b>: {stats[5]['value']}</div>
                </div>
                <div className="statistics">
                    <div className='divInner'><b>{stats[6]['stats']}</b>: {stats[6]['value']}</div>
                    <div className='divInner'><b>{stats[7]['stats']}</b>: {stats[7]['value']}</div>
                    <div className='divInner'><b>{stats[8]['stats']}</b>: {stats[8]['value']}</div>
                    <div className='divInner'><b>{stats[9]['stats']}</b>: {stats[9]['value']}</div>
                    <div className='divInner'><b>{stats[10]['stats']}</b>: {stats[10]['value']}</div>
                    <div className='divInner'><b>{stats[11]['stats']}</b>: {stats[11]['value']}</div>
                </div>
            </div>
        </>
    )
}

export default Simulator
