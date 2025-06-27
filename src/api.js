import axios from "axios";
const API = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api"
});
export default API;