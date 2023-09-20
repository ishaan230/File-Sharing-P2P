// import { useState } from "react";
import styles from "./Header.css";

const Header = (props) => {


    return ( <nav className= "navBar">
        <ul className= "list">
            <li onClick={() => {props.showUpload(true)}}>Upload</li>
            <li onClick={() => {props.showDownload(true)}}>Download</li>
        </ul>
    </nav> );
}
 
export default Header;