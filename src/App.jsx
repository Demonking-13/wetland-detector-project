import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './routes/home';
import UploadPage from "./routes/upload";


function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
