import { useDropzone } from "react-dropzone";
import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../templates/dropbox.css'

const Dropzone = () => {
    const [file, setFiles] = useState([]);
    const navigate = useNavigate();

    // Accept only image files
    const onDrop = useCallback((acceptedFiles) => {
        setFiles(
            acceptedFiles.map((file) =>
                Object.assign(file, { preview: URL.createObjectURL(file) })
            )

        );
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.jpg', '.jpeg', '.png'] },
        multiple: false, // Allow only a single file at a time
    });

    // Navigate to the upload page when the button is clicked
    const handleAnalyze = () => {
        if (file) {
            navigate("/upload", { state: { file } });
        }
    };


    return (
        <div className="dropzone-container">

            <div className="uploadbox">
                <div {...getRootProps()} className="dropzone-box" >
                    <input {...getInputProps()} />
                    {isDragActive ? (
                        <p>Drop the files here...</p>
                    ) : (
                        <p>Drop your files here</p>
                    )}

                    {file.length > 0 && (
                        <div className="preview-container">
                            {file.map((file) => (
                                <img key={file.name} src={file.preview} alt="preview" className="preview-image" />
                            ))}
                        </div>
                    )}
                </div>
            </div>
            {file && <button onClick={handleAnalyze}>Analyse</button>}
        </div>
    );
};

export default Dropzone;