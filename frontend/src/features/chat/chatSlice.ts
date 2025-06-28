// frontend/src/features/chat/chatSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { ChatMessage } from '../../types';
import apiClient from '../../lib/api';
import { v4 as uuidv4 } from 'uuid';

interface ChatState {
  messages: ChatMessage[];
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: ChatState = {
  messages: [
    {
      id: uuidv4(),
      role: 'assistant',
      content: 'Hola, soy tu Asesor IA. ¿En qué puedo ayudarte hoy?',
    },
  ],
  status: 'idle',
  error: null,
};

export const postQuery = createAsyncThunk(
  'chat/postQuery',
  async (question: string) => {
    // Apunta al endpoint RAG. Podríamos crear otro thunk para el endpoint general.
    const response = await apiClient.post('/rag/query', { question });
    return response.data.answer;
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(postQuery.pending, (state, action) => {
        state.status = 'loading';
        state.messages.push({ id: uuidv4(), role: 'user', content: action.meta.arg });
        state.messages.push({ id: uuidv4(), role: 'assistant', content: '', isLoading: true });
      })
      .addCase(postQuery.fulfilled, (state, action: PayloadAction<string>) => {
        state.status = 'succeeded';
        const lastMessage = state.messages[state.messages.length - 1];
        if (lastMessage && lastMessage.isLoading) {
          lastMessage.content = action.payload;
          lastMessage.isLoading = false;
        }
      })
      .addCase(postQuery.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message ?? 'Ocurrió un error desconocido.';
        const lastMessage = state.messages[state.messages.length - 1];
        if (lastMessage && lastMessage.isLoading) {
          lastMessage.content = 'Lo siento, ha ocurrido un error al procesar tu pregunta.';
          lastMessage.isLoading = false;
        }
      });
  },
});

export default chatSlice.reducer;
