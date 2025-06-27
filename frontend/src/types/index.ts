// frontend/src/types/index.ts

// Define el tipo para un único mensaje en el historial del chat.
// Esto nos da seguridad y autocompletado en todo el código.
export interface ChatMessage {
  id: string; // Un ID único para cada mensaje
  role: 'user' | 'assistant' | 'system'; // Quién envió el mensaje
  content: string; // El texto del mensaje
  isLoading?: boolean; // Opcional: para mostrar un indicador de carga
}
