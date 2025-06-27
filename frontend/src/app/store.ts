// frontend/src/app/store.ts
import { configureStore } from '@reduxjs/toolkit';
import chatReducer from '../features/chat/chatSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    // Aquí podríamos añadir otros reducers en el futuro
  },
});

// Inferimos los tipos `RootState` y `AppDispatch` del propio store.
// Esto es una buena práctica de TypeScript para usar en toda la app.
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
