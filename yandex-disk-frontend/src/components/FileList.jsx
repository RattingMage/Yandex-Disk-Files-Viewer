import React, { useState, useEffect  } from 'react';
import { getFiles, downloadFiles, getCsrfToken } from '../api';

// Компонент для отображения списка файлов
const FileList = () => {
    const [publicKey, setPublicKey] = useState('');
    const [fileType, setFileType] = useState('all');
    const [files, setFiles] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [error, setError] = useState('');

    // Веб-хук для подгрузки CSRF-токена
    useEffect(() => {
        getCsrfToken();
    }, []);

    // Обработчик кнопки "View Files"
    const handleViewFiles = async () => {
        try {
            const data = await getFiles(publicKey, fileType);
            setFiles(data.files);
            setError('');
        } catch (err) {
            setError('Не удалось получить список файлов');
        }
    };

    // Обработчик кнопки "Download Selected Files"
    const handleDownloadFiles = async () => {
        if (selectedFiles.length === 0) {
            setError('Выберите хотя бы один файл для загрузки');
            return;
        }

        try {
            const blob = await downloadFiles(publicKey, selectedFiles);
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'downloaded_files.zip');
            document.body.appendChild(link);
            link.click();
            link.remove();
            setError('');
        } catch (err) {
            setError('Не удалось загрузить файлы');
        }
    };

    // Обработчик для выбора типов файлов
    const handleFileSelect = (filePath) => {
        if (selectedFiles.includes(filePath)) {
            setSelectedFiles(selectedFiles.filter((path) => path !== filePath));
        } else {
            setSelectedFiles([...selectedFiles, filePath]);
        }
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Yandex Disk Files Viewer</h1>
            <div className="mb-3">
                <label className="form-label">Public Key:</label>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Enter public key"
                        value={publicKey}
                        onChange={(e) => setPublicKey(e.target.value)}
                    />
            </div>
            <div className="mb-3">
                <label className="form-label">Filter by File Type:</label>
                    <select
                        className="form-select"
                        value={fileType}
                        onChange={(e) => setFileType(e.target.value)}
                    >
                        <option value="all">All Files</option>
                        <option value="image">Images</option>
                        <option value="document">Documents</option>
                        <option value="audio">Audio</option>
                        <option value="video">Video</option>
                    </select>
            </div>
            <button className="btn btn-primary mb-3" onClick={handleViewFiles}>View Files</button>
            {error && <div className="alert alert-danger">{error}</div>}
            {files.length > 0 && (
                <div className="card">
                    <div className="card-body">
                        <h2 className="card-title">Files:</h2>
                        <ul className="list-group">
                            {files.map((file) => (
                                <li key={file.path} className="list-group-item">
                                    <div className="form-check">
                                        <input
                                                class="form-check-input"
                                                type="checkbox"
                                                checked={selectedFiles.includes(file.path)}
                                                onChange={() => handleFileSelect(file.path)}
                                            />
                                            <label className="form-check-label">
                                                {file.name} ({file.type})
                                            </label>
                                    </div>
                                </li>
                            ))}
                        </ul>
                        <button className="btn btn-success mt-3" onClick={handleDownloadFiles}>Download Selected Files</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FileList;