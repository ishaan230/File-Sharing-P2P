import { useState, useRef } from "react";
import "./Upload.css";
import { open } from '@tauri-apps/api/dialog';

const Upload = () => {

    const [fileName, setFileName] = useState("");
    const [uploadMessage, setUploadMessage] = useState("");

    const inputRef = useRef(null);

    const fileChange = (e) => {
        setFileName(e.target.value);
    }

    const handleUpload = (e) => {
        console.log("Send upload request for ", fileName);
    }

    const handleFileSelection = async (e) => {
        // Open a selection dialog for image files
        console.log("OK")
        const selected = await open({
          multiple: false,
          title: "Select file"
        });

        if(selected){
            console.log(selected)
            inputRef.current.value = selected
            setFileName(selected)
        }
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
      <button onClick={handleFileSelection}>Select File</button>
      <input type="text" placeholder="Enter file path..." ref={inputRef} onChange={fileChange}/> 
      <button type="submit" onClick={handleUpload}>Upload</button>
    </form>
    </div>);
}
 
export default Upload;
