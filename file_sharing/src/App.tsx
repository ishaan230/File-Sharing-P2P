import React, { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";

function App() {
  const [name, setName] = useState("Welcome to File sharing P2P!!");

  async function sendFile() {
    // Add your logic here for sending files
    // For example, you can invoke Tauri functions if needed
    // await invoke("sendFileFunction", { /* parameters */ });
    setName("File Sent");
  }

  return (
    <div className="container">
      <h1>{name}</h1>
      <button className="button" type="button" onClick={sendFile}>
        Send File
      </button>
    </div>
  );
}

export default App;
