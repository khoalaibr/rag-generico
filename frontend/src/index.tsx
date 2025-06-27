// frontend/src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './app/store';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Al eliminar <React.StrictMode>, el componente del chat solo se montará
// una vez, creando una única conexión WebSocket estable y eliminando
// el falso mensaje de error de conexión.
root.render(
  // <React.StrictMode> // Comentamos o eliminamos esta línea
    <Provider store={store}>
      <App />
    </Provider>
  // </React.StrictMode> // Comentamos o eliminamos esta línea
);
