import axios, { AxiosInstance } from "axios"
import { ElMessage } from 'element-plus'

const apiClient: AxiosInstance = axios.create({
    baseURL: "http://localhost:5010",
    // リクエストヘッダ
    headers: {
        "Content-type": "application/json",
    },
})

apiClient.interceptors.response.use(
    response => {

      return response.data;
    },
    error => {
      let message = error.message;
      if (error.response.data && error.response.data.errors) {
        message = error.response.data.errors;
      } else if (error.response.data && error.response.data.error) {
        message = error.response.data.error;
      }
  
      ElMessage({
        message: message,
        type: 'error',
        duration: 5 * 1000,
      });
      return Promise.reject(error);
    }
  );
  

export default apiClient
