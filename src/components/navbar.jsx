import { useState } from "react";
import "../templates/navbar.css"


const Navbar = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    return (
        <nav className="navbar">
            <div className="logo"> Wetland & Dryland Detector</div>

            <div className="menu">
                {/* Dropdown for Tools */}
                <div className="dropdown">
                    <button
                        className="dropdown-btn"
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                    >
                        Tools ▼
                    </button>
                    {isDropdownOpen && (
                        <div className="dropdown-menu">
                            <p className="dropdown-item">Tool 1</p>
                            <p className="dropdown-item">Tool 2</p>
                        </div>
                    )}
                </div>
                <a href="#" className="menu-item">API</a>
                <a href="#" className="menu-item">Home</a>
                <a href="#" className="menu-item">Contacts</a>
                <button className="sign-btn">Sign-in / Sign-up</button>
            </div>
        </nav>
    );
};

export default Navbar;