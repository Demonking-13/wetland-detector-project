import FileUpload from "../components/FileUpload";
import "../styles/Home.css";
import Navbar from "../components/navbar";

const Home = () => {
  return (
    <div className="home-container">
      <Navbar />
      <h1 className="upload-heading">UPLOAD SATELLITE IMAGE</h1>
      <FileUpload />
    </div>
  );
};

export default Home;
