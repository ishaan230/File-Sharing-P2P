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
      <Header showUpload = {changeUpload} showDownload = {changeDownload}/>
      {showDownload && <Download />}
      {showUpload && <Upload />}
    </>
  );
}

export default App;
