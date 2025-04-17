import { useEffect, useState } from 'react'
import './Simulator.css'
import data from './cycle.json'
import stats from './stats.json'
import { Link } from 'react-router-dom'

const Simulator = () => {
    const [index, setIndex] = useState(0)
    const [value, setValue] = useState(-1)

    useEffect(() => {
        // Handle stage highlighting
        const stages = ["fetch", "decode", "execute", "memory", "writeback"]
        const stageElements = [".div1", ".div2", ".div3", ".div4", ".div5"]

        stages.forEach((stage, i) => {
            const element = document.querySelector(stageElements[i])
            if (element) {
                if (data[index][stage] === -1) {
                    element.classList.add("glow")
                } else {
                    element.classList.remove("glow")
                }
            }
        })

        // Handle forwarding
        const handleForwarding = () => {
            const forwardingValue = data[index]["forwarding"]
            const targetValue = data[index]["value"]
            const existingDiv = document.querySelector('.newDiv')
            
            if (existingDiv) {
                existingDiv.remove()
            }

            if (forwardingValue !== -1) {
                const targetStages = [".div1", ".div2", ".div3", ".div4", ".div5"]
                const targetIndex = 4 - forwardingValue
                
                if (targetIndex >= 0 && targetIndex < targetStages.length) {
                    setValue(targetIndex)
                    const divElement = document.createElement('div')
                    divElement.textContent = targetValue
                divElement.className = 'newDiv'
                    const targetElement = document.querySelector(targetStages[targetIndex])
                    if (targetElement) {
                        targetElement.appendChild(divElement)
                    }
                }
            } else {
                setValue(-1)
            }
        }

        handleForwarding()
    }, [index])

    const stepHandler = () => {
        if (index < data.length - 1) setIndex(index + 1)
    }

    const prevHandler = () => {
        if (index >= 1) setIndex(index - 1)
    }

    return (
        <div className="complete" style={{ height: '100vh' }}>
            {/* Header section */}
            <div className="box">
                <Link to="/register">
                    <button 
                        type="button" 
                        className="btn btn-outline-secondary back-button"
                        style={{ paddingLeft: '30px', paddingRight: '30px' }}
                    >
                        Back
                    </button>
                    </Link>
                <div className="topbar">CPU Pipeline Simulator</div>
            </div>

            {/* Control buttons */}
            <div className="runButtons">
                <button
                    type="button"
                    className="btn btn-outline-danger step-button"
                    style={{ marginRight: '40px', paddingLeft: '50px', paddingRight: '50px' }}
                    onClick={stepHandler}
                >
                    Step
                </button>
                <button
                    type="button"
                    className="btn btn-outline-danger prev-button"
                    style={{ paddingLeft: '50px', paddingRight: '50px' }}
                    onClick={prevHandler}
                >
                    Prev
                </button>
            </div>

            {/* Pipeline stages */}
            <div className="pipeline-container">
                {/* IF Stage */}
                <div className="stage-container">
                    <div className="inner div1">
                        <div className="stage-label">IF</div>
                        <div className="data1" style={{ width: '100%' }}>
                            <b>{data[index]['fetch']}</b>
                        </div>
                    </div>
                    <div className="buffer-register">
                        <div className="buffer-label">IF/ID</div>
                        <div className="arrow-right" />
                    </div>
                </div>

                {/* ID Stage */}
                <div className="stage-container">
                    <div className="inner div2">
                        <div className="stage-label">ID</div>
                        <div className="data2" style={{ width: '100%' }}>
                            <b>{data[index]['decode']}</b>
                        </div>
                </div>
                    <div className="buffer-register">
                        <div className="buffer-label">ID/EX</div>
                        <div className="arrow-right" />
                    </div>
                </div>

                {/* EX Stage */}
                <div className="stage-container">
                    <div className="inner div3">
                        <div className="stage-label">EX</div>
                        <div className="data3" style={{ width: '100%' }}>
                            <b>{data[index]['execute']}</b>
                        </div>
                    </div>
                    <div className="buffer-register">
                        <div className="buffer-label">EX/MEM</div>
                        <div className="arrow-right" />
                    </div>
                </div>

                {/* MEM Stage */}
                <div className="stage-container">
                    <div className="inner div4">
                        <div className="stage-label">MEM</div>
                        <div className="data4" style={{ width: '100%' }}>
                            <b>{data[index]['memory']}</b>
                        </div>
                    </div>
                    <div className="buffer-register">
                        <div className="buffer-label">MEM/WB</div>
                        <div className="arrow-right" />
                    </div>
                </div>

                {/* WB Stage */}
                <div className="stage-container">
                    <div className="inner div5">
                        <div className="stage-label">WB</div>
                        <div className="data5" style={{ width: '100%' }}>
                            <b>{data[index]['writeback']}</b>
                        </div>
                </div>
                </div>
            </div>

            {/* Statistics section */}
            <div className="stats-header">Performance Statistics</div>
            
            {/* First row of statistics */}
            <div className="statistics">
                {stats.slice(0, 6).map((stat, i) => (
                    <div className="stat-card" key={i}>
                        <div className="stat-name">
                            <b>{stat.stats}</b>
                        </div>
                        <div className="stat-value">{stat.value}</div>
                    </div>
                ))}
            </div>
            
            {/* Second row of statistics */}
            <div className="statistics">
                {stats.slice(6, 12).map((stat, i) => (
                    <div className="stat-card" key={i + 6}>
                        <div className="stat-name">
                            <b>{stat.stats}</b>
                        </div>
                        <div className="stat-value">{stat.value}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Simulator
