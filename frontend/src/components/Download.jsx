import { useState } from "react";
import "./Download.css";

const Download = () => {

  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

    return ( <div className="down-container">

    <h1>{greetMsg}</h1>

    <form
      className="row"
      onSubmit={(e) => {
        e.preventDefault();
        setTimeout(() => {setGreetMsg("File " + name + " downloaded.");}, 1000);
      }}
    >
      <input
        id="greet-input"
        onChange={(e) => setName(e.currentTarget.value)}
        placeholder="Enter a filename..."
      />
      <button type="submit">Search</button>
    </form>
  </div> );
}
 
export default Download;