// frontend/src/features/chat/Chat.tsx
import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faRobot, faUser, faCircleNotch } from '@fortawesome/free-solid-svg-icons';
import { useAppSelector, useAppDispatch } from '../../app/hooks';
import { postQuery } from './chatSlice';
import type { ChatMessage } from '../../types';

const Message: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isAssistant = message.role === 'assistant';
  return (
    <div className={`flex items-start gap-3 my-4 ${isAssistant ? '' : 'flex-row-reverse'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isAssistant ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
        <FontAwesomeIcon icon={isAssistant ? faRobot : faUser} />
      </div>
      <div className={`relative px-4 py-2 rounded-lg max-w-xl ${isAssistant ? 'bg-muted' : 'bg-primary text-primary-foreground'}`}>
        {message.isLoading ? (
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0s' }}></span>
            <span className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
            <span className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
          </div>
        ) : (
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        )}
      </div>
    </div>
  );
};

export const Chat = () => {
  const dispatch = useAppDispatch();
  const { messages, status } = useAppSelector((state) => state.chat);
  const [currentMessage, setCurrentMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentMessage.trim() && status !== 'loading') {
      dispatch(postQuery(currentMessage.trim()));
      setCurrentMessage('');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background font-sans">
      <header className="p-4 border-b"><h1 className="text-xl font-bold text-foreground">Asesor IA (Modo Estable HTTP)</h1></header>
      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          {messages.map((msg) => (<Message key={msg.id} message={msg} />))}
          <div ref={messagesEndRef} />
        </div>
      </main>
      <footer className="p-4 border-t bg-background">
        <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto flex items-center gap-4">
          <input type="text" value={currentMessage} onChange={(e) => setCurrentMessage(e.target.value)} placeholder="Escribe tu pregunta aquí..." className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-ring focus:outline-none bg-input text-foreground" disabled={status === 'loading'} />
          <button type="submit" className="p-3 w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-colors" disabled={status === 'loading' || !currentMessage.trim()}>
            {status === 'loading' ? <FontAwesomeIcon icon={faCircleNotch} className="animate-spin" /> : <FontAwesomeIcon icon={faPaperPlane} />}
          </button>
        </form>
      </footer>
    </div>
  );
};
