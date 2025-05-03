import { useState, useRef, useEffect } from "react";

export const QAChat = () => {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>(
    [],
  );
  const [newQuestion, setNewQuestion] = useState("");

  // Reference to the message container
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Scroll to the bottom when a new message is added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSubmit = () => {
    if (newQuestion.trim()) {
      setMessages((prev) => [
        ...prev,
        { text: newQuestion, isUser: true },
        {
          text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
          isUser: false,
        },
      ]);
      setNewQuestion("");
    }
  };

  return (
    <div className="mt-2 flex h-full flex-col overflow-hidden rounded-md bg-white/60 p-4 shadow-md backdrop-blur-md dark:bg-black/60">
      {/* Scrollable messages */}
      <div className="hide-scrollbar flex-1 overflow-y-auto pr-1">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.isUser ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-xs rounded-lg p-3 shadow md:max-w-md ${
                msg.isUser
                  ? "bg-gray-500 text-white"
                  : "bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100"
              }`}
            >
              {msg.text}
            </div>
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
