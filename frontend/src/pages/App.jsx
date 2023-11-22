import { useEffect, useState } from "react";
import Header from "../components/Header";
import "./App.css";
import Download from "../components/Download";
import Upload from "../components/Upload";

function App() {

  const [showUpload, setShowUpload] = useState(true);
  const [showDownload, setShowDownload] = useState(false);

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
