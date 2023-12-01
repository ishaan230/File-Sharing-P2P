import axios from "axios";

const { app } = window.tauri;

window.tauri.promisified({
  cmd: 'beforeClose',
  resolve: async () => {
     axios.get("") 
  },
});
