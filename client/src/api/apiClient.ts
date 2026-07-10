import axios from "axios";

const axiosApiClient = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  timeout: 10000,
  headers: {
    Accept: "application/json",
  },
});

axiosApiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("authtoken");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default axiosApiClient;
