import React, { createContext, useContext, useState, useCallback } from 'react';

export interface FileAttachment {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  files?: FileAttachment[];
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

interface ChatContextType {
  chats: Chat[];
  currentChatId: string | null;
  currentChat: Chat | null;
  isLoading: boolean;
  createNewChat: () => void;
  selectChat: (chatId: string) => void;
  sendMessage: (content: string, files?: FileAttachment[]) => Promise<void>;
  deleteChat: (chatId: string) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Mock chat history
const mockChats: Chat[] = [
  {
    id: '1',
    title: 'Apple Inc. Annual Report 2023',
    messages: [
      {
        id: '1-1',
        role: 'user',
        content: 'Please analyze this annual report and generate an ESG report.',
        files: [{ id: 'f1', name: 'Apple_Annual_Report_2023.pdf', size: 2500000, type: 'application/pdf', file: new File([], 'Apple_Annual_Report_2023.pdf') }],
        timestamp: new Date('2024-01-15T10:30:00'),
      },
      {
        id: '1-2',
        role: 'assistant',
        content: `# ESG Report: Apple Inc. 2023

## Environmental Performance
- **Carbon Neutrality**: Apple achieved carbon neutrality for corporate operations
- **Renewable Energy**: 100% renewable energy across global facilities
- **Product Recycling**: Expanded recycling programs with Daisy robot processing 1.2M devices

## Social Responsibility
- **Workforce Diversity**: Increased representation in leadership roles
- **Supplier Standards**: Enhanced audits across 900+ suppliers
- **Community Investment**: $100M+ in education initiatives

## Governance
- **Board Independence**: 87.5% independent board members
- **Executive Compensation**: Tied to ESG performance metrics
- **Risk Management**: Comprehensive climate risk assessment framework`,
        timestamp: new Date('2024-01-15T10:31:00'),
      },
    ],
    createdAt: new Date('2024-01-15T10:30:00'),
    updatedAt: new Date('2024-01-15T10:31:00'),
  },
  {
    id: '2',
    title: 'Tesla Q4 Sustainability Review',
    messages: [],
    createdAt: new Date('2024-01-14T14:20:00'),
    updatedAt: new Date('2024-01-14T14:25:00'),
  },
  {
    id: '3',
    title: 'Microsoft ESG Analysis',
    messages: [],
    createdAt: new Date('2024-01-12T09:15:00'),
    updatedAt: new Date('2024-01-12T09:45:00'),
  },
];

// API configuration - use localhost for cookie auth
const API_BASE = 'http://localhost:8080';

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingChats, setIsLoadingChats] = useState(true);

  // Load conversations from database on mount
  React.useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setIsLoadingChats(true);
      const response = await fetch(`${API_BASE}/conversations`, {
        credentials: 'include',
      });

      if (response.ok) {
        const conversations = await response.json();
        // Convert backend format to frontend format
        const formattedChats: Chat[] = conversations.map((conv: any) => ({
          id: conv.id.toString(),
          title: conv.title,
          messages: [], // Messages loaded separately when chat is selected
          createdAt: new Date(conv.created_at),
          updatedAt: new Date(conv.updated_at),
        }));
        setChats(formattedChats);
      } else {
        console.error('Failed to load conversations');
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    } finally {
      setIsLoadingChats(false);
    }
  };

  const currentChat = chats.find(c => c.id === currentChatId) || null;

  const createNewChat = useCallback(() => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'New ESG Analysis',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  }, []);

  const selectChat = useCallback(async (chatId: string) => {
    setCurrentChatId(chatId);

    // Load messages for this conversation
    try {
      const response = await fetch(`${API_BASE}/conversations/${chatId}`, {
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        // Update chat with messages
        setChats(prev => prev.map(chat => {
          if (chat.id === chatId) {
            return {
              ...chat,
              messages: data.messages.map((msg: any) => ({
                id: msg.id.toString(),
                role: msg.role,
                content: msg.content,
                files: msg.file_name ? [{
                  id: msg.id.toString(),
                  name: msg.file_name,
                  size: 0,
                  type: 'application/pdf',
                  file: new File([], msg.file_name)
                }] : undefined,
                timestamp: new Date(msg.created_at),
              })),
            };
          }
          return chat;
        }));
      }
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  }, []);

  const sendMessage = useCallback(async (content: string, files?: FileAttachment[]) => {
    setIsLoading(true);

    try {
      let activeConversationId = currentChatId;

      // Prepare request based on whether we have files
      let response;
      if (files && files.length > 0) {
        // File upload
        const formData = new FormData();
        formData.append('file', files[0].file);
        if (currentChatId) {
          formData.append('conversation_id', currentChatId);
        }

        response = await fetch(`${API_BASE}/chat/file`, {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });
      } else {
        // Text message
        response = await fetch(`${API_BASE}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: content,
            conversation_id: currentChatId ? parseInt(currentChatId) : null,
          }),
          credentials: 'include',
        });
      }

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
      }

      const data = await response.json();
      activeConversationId = data.conversation_id.toString();

      // If this was a new conversation, set it as current
      if (!currentChatId) {
        setCurrentChatId(activeConversationId);
      }

      // Reload conversations to get the updated one
      await loadConversations();

      // Load messages for the active conversation
      await selectChat(activeConversationId);

    } catch (error) {
      console.error('Error sending message:', error);
      // Show error to user
      const errorMessage: Message = {
        id: `msg-${Date.now()}-error`,
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to send message'}`,
        timestamp: new Date(),
      };

      setChats(prev => prev.map(chat => {
        if (chat.id === currentChatId) {
          return {
            ...chat,
            messages: [...chat.messages, errorMessage],
          };
        }
        return chat;
      }));
    } finally {
      setIsLoading(false);
    }
  }, [currentChatId, loadConversations, selectChat]);

  const deleteChat = useCallback(async (chatId: string) => {
    try {
      const response = await fetch(`${API_BASE}/conversations/${chatId}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      if (response.ok) {
        // Remove chat from frontend
        setChats(prev => prev.filter(c => c.id !== chatId));
        if (currentChatId === chatId) {
          setCurrentChatId(null);
        }
      } else {
        console.error('Failed to delete conversation');
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  }, [currentChatId]);

  return (
    <ChatContext.Provider value={{
      chats,
      currentChatId,
      currentChat,
      isLoading,
      createNewChat,
      selectChat,
      sendMessage,
      deleteChat,
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
