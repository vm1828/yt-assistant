// TODO: refactor

import { getConversationByVideoId } from "@/api";
import { postChatMessage } from "@/api/chat";
import { useVideoStore } from "@/store";
import { Conversation } from "@/types";
import { useAuth0 } from "@auth0/auth0-react";
import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

export const QAChat = () => {
  const [conversation, setConversation] = useState<Conversation>({
    id: "",
    video_id: "",
    messages: [],
  });
  const [newQuestion, setNewQuestion] = useState("");

  // Reference to the message container
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const { getAccessTokenSilently } = useAuth0();
  const { currentVideo, conversationCache, setCurrentConversation } =
    useVideoStore();

  // Show cached conversation immediately when currentVideo changes
  useEffect(() => {
    if (!currentVideo) return;

    const fetchConversation = async () => {
      if (conversationCache[currentVideo.id]) {
        setConversation(conversationCache[currentVideo.id]);
      } else {
        const token = await getAccessTokenSilently();
        const conv = await getConversationByVideoId(currentVideo.id, token);
        setConversation(conv);
      }
    };

    fetchConversation();
  }, [currentVideo, conversationCache, getAccessTokenSilently]);

  // Scroll to the bottom when new message is added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ block: "end" });
    }
  }, [conversation.messages]);

  // Update conversation with new messages
  useEffect(() => {
    if (!conversation?.id) return;
    setCurrentConversation(conversation);
  }, [conversation, setCurrentConversation]);

  const handleSubmit = async () => {
    if (!newQuestion.trim() || !conversation.id) return;

    const token = await getAccessTokenSilently();

    // optimistic UI update
    const tempMessage = {
      user_message: newQuestion,
      ai_response: "...",
    };
    setConversation((prev) => ({
      ...prev,
      messages: [...(prev.messages || []), tempMessage],
    }));

    setNewQuestion("");

    try {
      const response = await postChatMessage(
        conversation.id,
        newQuestion,
        token,
      );
      setConversation((prev) => {
        const updatedMessages = [...(prev.messages || [])];
        const lastIndex = updatedMessages.length - 1;

        if (lastIndex >= 0) {
          updatedMessages[lastIndex] = {
            ...updatedMessages[lastIndex],
            ai_response: response.ai_response, // only replace the response text
          };
        }

        return {
          ...prev,
          messages: updatedMessages,
        };
      });
    } catch {
      setConversation((prev) => ({
        ...prev,
        messages: [
          ...(prev.messages || []),
          { user_message: "", ai_response: "Error: failed to send message." },
        ],
      }));
    }
  };

  return (
    <div className="mt-2 flex h-full flex-col overflow-hidden rounded-md bg-white/60 p-4 shadow-md backdrop-blur-md dark:bg-black/60">
      {/* Scrollable messages */}
      <div className="hide-scrollbar min-h-0 flex-1 overflow-y-auto pr-1 text-xs">
        {conversation.messages.map((msg) => (
          <div key={msg.id} className="flex flex-col gap-1">
            {/* User message */}
            {msg.user_message && (
              <div className="flex justify-end">
                <div className="mb-1 min-w-3/12 rounded-lg bg-gray-500 p-3 text-white shadow md:max-w-md">
                  {msg.user_message}
                </div>
              </div>
            )}
            {/* AI response */}
            {msg.ai_response && (
              <div className="flex justify-start">
                <div className="mb-2 min-w-12/12 overflow-x-auto rounded-lg bg-gray-200 p-3 text-gray-800 shadow md:max-w-md dark:bg-gray-700 dark:text-gray-100">
                  {msg.ai_response === "..." ? (
                    <span className="animate-pulse text-xl font-bold text-gray-500">
                      ...
                    </span>
                  ) : (
                    <ReactMarkdown
                      remarkPlugins={[remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {msg.ai_response}
                    </ReactMarkdown>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="mt-2 flex flex-shrink-0 space-x-2">
        <input
          type="text"
          value={newQuestion}
          onChange={(e) => setNewQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="Ask a question..."
          className="input-field"
        />
        <button onClick={handleSubmit} className="button-action">
          Ask
        </button>
      </div>
    </div>
  );
};
