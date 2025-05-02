import axios from "axios";

const apiHost = import.meta.env.VITE_API_HOST!;
const apiPort = import.meta.env.VITE_API_PORT!;

export const apiClient = axios.create({
  baseURL: `http://${apiHost}:${apiPort}`,
  headers: {
    "Content-Type": "application/json",
  },
});
