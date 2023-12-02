import { useState, useRef, useEffect } from "react";
import "./Upload.css";
import { open } from '@tauri-apps/api/dialog';
import axios from "axios";

const Upload = () => {

    const SERVER = "http://127.0.0.1:5000"
    const [upd, setUpd] = useState(false)
    useEffect(()=>{
        if(!upd){
            axios.put(`${SERVER}/update`)
                .then((res)=>{
                    console.log(res)
                })
                .catch((err)=>{
                })
            setUpd(true)
        }
    }, [])

    const [fileName, setFileName] = useState("");
    const [uploadMessage, setUploadMessage] = useState("");

    const inputRef = useRef(null);

    const fileChange = (e) => {
        setFileName(e.target.value);
    }

    const handleUpload = (_) => {
        console.log("Send upload request for ", fileName);
        axios.post(`${SERVER}/upload`, {"file":fileName})
            .then((res) => {
                console.log(res.data)
            })
            .catch((err)=>{
                console.log("Error", err)
                alert("No Active Peers found!")
                if(err.status_code == 404){
                    alert("No Active Peers found!")
                }
            })
    }

    const handleFileSelection = async (_) => {
        // Open a selection dialog for image files
        const selected = await open({
          multiple: false,
          title: "Select file"
        });

        if(selected){
            console.log(selected)
            inputRef.current.value = selected
            setFileName(selected)
        }else{
            alert("No file selected!")
        }
    }

    return ( <div className="up-container">

     <h1>{uploadMessage}</h1>   

    <form
      className="row"
      onSubmit={(e) => {
        e.preventDefault();
      }}
    >
      <button onClick={handleFileSelection}>
      </button>
      <input type="text" placeholder="Enter file path..." ref={inputRef} onChange={fileChange}/> 
      <button type="submit" onClick={handleUpload}>Upload</button>
    </form>
    </div>);
}
 
export default Upload;
