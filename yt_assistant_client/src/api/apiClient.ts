import axios from "axios";

const apiHost = import.meta.env.VITE_API_HOST!;
const apiPort = import.meta.env.VITE_API_PORT!;

const apiClient = axios.create({
  baseURL: `http://${apiHost}:${apiPort}`,
  headers: {
    "Content-Type": "application/json",
  },
});

// // Interceptor for logging requests during development/debugging.
// apiClient.interceptors.request.use(
//   (config) => {
//     console.log("Request made with config:", config);
//     return config;
//   },
//   (error) => {
//     console.error("Request Error:", error);
//     return Promise.reject(error);
//   }
// );

export default apiClient;
