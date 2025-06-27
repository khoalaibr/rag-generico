// frontend/src/lib/api.ts
import axios from 'axios';

// Creamos una instancia de axios con la configuración base.
const apiClient = axios.create({
  // La URL base de nuestra API del backend.
  baseURL: 'http://localhost:8000/api/v1', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
