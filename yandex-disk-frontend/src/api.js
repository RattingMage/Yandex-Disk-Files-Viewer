import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = 'http://localhost:8000';

// Настройка axios для автоматического включения CSRF-токена в заголовки
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.withCredentials = true;

// Запрос для получения CSRF-токена.
export const getCsrfToken = async () => {
    const response = await axios.get(`${API_BASE_URL}/get-csrf-token/`);
    return response.data.csrfToken;
};

// Запрос для отображения списка файлов с Яндекс.Диска.
export const getFiles = async (publicKey, fileType) => {
    const config = {
        headers:{
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
    const response = await axios.post(`${API_BASE_URL}/get_files/`, {
        public_key: publicKey,
        file_type: fileType,
    }, config);
    return response.data;
};

// Запрос для загрузки выбранных файлов с Яндекс.Диска.
export const downloadFiles = async (publicKey, filePaths) => {
    const config = {
        headers:{
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        responseType: 'blob'
      }
    const response = await axios.post(`${API_BASE_URL}/download/`, {
        public_key: publicKey,
        file_paths: filePaths,
    }, config);
    return response.data;
};