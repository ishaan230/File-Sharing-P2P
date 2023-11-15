import { useState } from "react";
import "./Upload.css";

const Upload = () => {

    const [fileName, setFileName] = useState("");
    const [uploadMessage, setUploadMessage] = useState("");

    const fileChange = (e) => {
        setFileName(e.target.files[0].name);
    }

    const handleUpload = (e) => {
        console.log("Send upload request for ", fileName);
    }

    return ( <div className="up-container">

     <h1>{uploadMessage}</h1>   

    <form
      className="row"
      onSubmit={(e) => {
        e.preventDefault();
        setTimeout(() => {setUploadMessage("File " + fileName + " uploaded.");}, 1000);
      }}
    >
      <input
        type = "file"
        placeholder="Enter a filename..."
        onChange= {fileChange}
      />
      <button type="submit" onClick={handleUpload}>Upload</button>
    </form>
    </div>);
}
 
export default Upload;
