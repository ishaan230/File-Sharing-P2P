import { useState, useEffect } from "react";
import "./Download.css";
import axios from "axios";

const Download = () => {

    const SERVER = "http://127.0.0.1:5000"
    const [data, setData] = useState([])
    useEffect(()=>{
        axios.put(`${SERVER}/update`)
            .then((res)=>console.log(res))
            .catch((err)=>console.log(err))
        axios.get(`${SERVER}/get_files`)
            .then((res)=>{
                console.log(res['data']['data'])
                // var data = res['data']['data']
                // data = data.filter((item) => item.name.trim() !== '')  
                setData(res['data']['data'])
            })
            .catch((err)=>console.log("done"))
    }, [])


  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

    const onButtonClick = (hash)=>{
        console.log(hash)
        axios.post(`${SERVER}/download/{hash}`)
            .then((res)=>{console.log(res)})
            .except((err)=>{console.log(err)})
    }

    return ( <div className='flex-container'>

    <h1>{greetMsg}</h1>

    {data.length > 0 ? (
        data.map((item, index) => (
            <div key={index} className="flex-item">
                <button className="button" onClick={() => onButtonClick(item.hash)}>{item.name}</button>
            </div>
        ))
      ) : (
        <p>No data available.</p>
      )}

      </div> );
}
 
export default Download;
