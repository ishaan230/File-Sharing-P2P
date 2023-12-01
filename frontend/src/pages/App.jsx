import { useEffect, useState } from "react";
import Header from "../components/Header";
import "./App.css";
import Download from "../components/Download";
import Upload from "../components/Upload";
import axios from "axios";

function App() {

  const SERVER = "http://127.0.0.1:5000"
  const [showUpload, setShowUpload] = useState(true);
  const [showDownload, setShowDownload] = useState(false);
  const [toggleUp, setToggle] = useState(false)

  const closeBtn = async () => {
          console.log("OKKK")
      if(!toggleUp){
          axios.put(`${SERVER}/deactivate`)
            .then((res)=>{
                alert("You are now inactive on the network")
                setToggle(true)
            })
            .catch((err)=>alert("something happened"))
      }else{
          axios.put(`${SERVER}/update`)
            .then((res)=>{
                alert("You are now active on the network")
                setToggle(false)
            })
            .catch((err)=>{
                alert("Some problem occured")
            })
      }
    };

  useEffect(()=>{
    axios.post(`${SERVER}/startup`)
      .then((res)=>{
        console.log(res)
      })
      .catch((err)=>{
        console.log(err)
      })
  },[])

  const changeUpload = (s) => {
    setShowUpload(s);
    setShowDownload(!s);
  }

  const changeDownload = (s) => {
    setShowUpload(!s);
    setShowDownload(s);
  }

  return (
    <>
      <button onClick={closeBtn}>{toggleUp?"Activate":"Deactivate"}</button>
      <Header showUpload = {changeUpload} showDownload = {changeDownload}/>
      {showDownload && <Download />}
      {showUpload && <Upload />}
    </>
  );
}

export default App;
