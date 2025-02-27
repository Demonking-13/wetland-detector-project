import Navbar from '../components/navbar'
import Dropbox from '../components/dropbox'
import "../templates/home.css"

function Home() {

    return (
        <>
            <Navbar />
            <div className='container'>
                <h1>UPLOAD SATELLITE IMAGE</h1>
                <Dropbox />
            </div>

        </>
    )

}

export default Home